package com.arafat.assistant;

import org.json.*;
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.security.*;
import java.security.spec.RSAPublicKeySpec;
import java.math.BigInteger;
import java.util.*;
import java.util.concurrent.atomic.AtomicBoolean;

/** Pure protocol helpers, independently testable without an Android device. */
public final class Protocol {
    private Protocol() {}
    public static final String ISSUER = "https://auth.openai.com";
    public static final String RESOURCE = "https://api.openai.com/v1";
    public static final String SCOPE = "openid profile email offline_access resource.invoke chatgpt.tokens.use.direct";
    public static String random() { byte[] bytes=new byte[48]; new SecureRandom().nextBytes(bytes); return b64(bytes); }
    public static String b64(byte[] bytes) { return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes); }
    public static String challenge(String verifier) throws Exception { return b64(MessageDigest.getInstance("SHA-256").digest(verifier.getBytes(StandardCharsets.US_ASCII))); }
    public static String form(Map<String,String> values) throws Exception {
        StringJoiner j=new StringJoiner("&");
        for(Map.Entry<String,String> e:values.entrySet()) j.add(URLEncoder.encode(e.getKey(),"UTF-8")+"="+URLEncoder.encode(e.getValue(),"UTF-8"));
        return j.toString();
    }
    public static final class Declined extends IOException { Declined() { super("Sign-in was declined. No connection was changed."); } }
    public static Map<String,String> callback(String target,String state,String existing) throws Exception {
        URI uri=new URI(target);
        if(target.length()>16000 || uri.isAbsolute() || !"/auth/callback".equals(uri.getPath())) throw new IOException("Invalid callback");
        Map<String,String> p=new HashMap<>();
        for(String pair:Objects.requireNonNullElse(uri.getRawQuery(),"").split("&")) {
            String[] kv=pair.split("=",2);
            String k=URLDecoder.decode(kv[0],"UTF-8"),v=URLDecoder.decode(kv.length>1?kv[1]:"","UTF-8");
            if(p.put(k,v)!=null) throw new IOException("Repeated callback parameter");
        }
        if(!MessageDigest.isEqual(state.getBytes(StandardCharsets.UTF_8),p.getOrDefault("state","").getBytes(StandardCharsets.UTF_8))) throw new IOException("Invalid sign-in state");
        if(p.containsKey("error")) throw new Declined();
        String id=p.getOrDefault("client_id",existing);
        if(id==null || !id.matches("oaiapp_[A-Za-z0-9_-]{1,180}") || (existing!=null && !existing.equals(id)) || p.getOrDefault("code","").isEmpty()) throw new IOException("Incomplete or mismatched registration");
        p.put("client_id",id); return p;
    }
    public static JSONObject verify(String encoded,String client,String nonce,String expectedSub,JSONObject jwks,long now) throws Exception {
        String[] parts=encoded.split("\\.",-1);
        if(parts.length!=3) throw new IOException("Invalid identity");
        JSONObject header=new JSONObject(new String(Base64.getUrlDecoder().decode(parts[0]),StandardCharsets.UTF_8));
        if(!"RS256".equals(header.optString("alg"))) throw new IOException("Invalid signature algorithm");
        String kid=header.getString("kid"); JSONObject key=null;
        JSONArray keys=jwks.getJSONArray("keys");
        for(int i=0;i<keys.length();i++) {
            JSONObject k=keys.getJSONObject(i);
            if(kid.equals(k.optString("kid")) && "RSA".equals(k.optString("kty"))) { if(key!=null) throw new IOException("Ambiguous key"); key=k; }
        }
        if(key==null || (!key.optString("alg","RS256").equals("RS256")) || !key.optString("use","sig").equals("sig")) throw new IOException("Unknown signing key");
        RSAPublicKeySpec spec=new RSAPublicKeySpec(new BigInteger(1,Base64.getUrlDecoder().decode(key.getString("n"))),new BigInteger(1,Base64.getUrlDecoder().decode(key.getString("e"))));
        Signature signature=Signature.getInstance("SHA256withRSA"); signature.initVerify(KeyFactory.getInstance("RSA").generatePublic(spec));
        signature.update((parts[0]+"."+parts[1]).getBytes(StandardCharsets.US_ASCII));
        if(!signature.verify(Base64.getUrlDecoder().decode(parts[2]))) throw new IOException("Identity signature rejected");
        JSONObject claims=new JSONObject(new String(Base64.getUrlDecoder().decode(parts[1]),StandardCharsets.UTF_8));
        Object aud=claims.get("aud"); boolean audience=client.equals(aud);
        if(aud instanceof JSONArray) for(int i=0;i<((JSONArray)aud).length();i++) audience|=client.equals(((JSONArray)aud).getString(i));
        if(!ISSUER.equals(claims.getString("iss")) || !audience || claims.getLong("exp")<now-30 || claims.getLong("iat")>now+30 || claims.optLong("nbf",0)>now+30 || claims.optString("sub").isEmpty()) throw new IOException("Identity claims rejected");
        if(nonce!=null && !nonce.equals(claims.optString("nonce"))) throw new IOException("Identity nonce rejected");
        if(expectedSub!=null && !expectedSub.equals(claims.getString("sub"))) throw new IOException("Account changed; sign out first");
        return claims;
    }
    public static boolean plan(JSONObject record) {
        Set<String> granted=new HashSet<>(Arrays.asList(record.optString("scope").split("\\s+")));
        return granted.contains("resource.invoke") && granted.contains("chatgpt.tokens.use.direct");
    }
    public static void check(AtomicBoolean cancelled) throws IOException { if(cancelled.get() || Thread.currentThread().isInterrupted()) throw new IOException("Task stopped."); }
    public static String error(String code,int status) {
        if(code.equals("subscription_sharing_user_not_eligible")) return "This account or workspace is not eligible. Reconnect using an eligible personal Plus or Pro account.";
        if(code.equals("subscription_sharing_not_enabled")) return "Reconnect and allow Use your ChatGPT plan.";
        if(code.equals("subscription_sharing_usage_unavailable")) return "ChatGPT plan usage is temporarily unavailable. Try again later.";
        if(status==429 || code.equals("subscription_sharing_usage_limit_exceeded")) return "Your ChatGPT usage or request limit was reached. Open Manage usage and check the reset time.";
        if(status==401 || status==403) return "ChatGPT rejected this connection. Sign in again and check your account and plan permission.";
        return "ChatGPT could not complete this request. Check your connection, account and model. No paid API fallback was used.";
    }
    public static JSONObject completed(Reader reader,AtomicBoolean cancelled) throws Exception {
        BufferedReader r=new BufferedReader(reader); String line; StringBuilder data=new StringBuilder(); int size=0;
        while((line=r.readLine())!=null) {
            check(cancelled); size+=line.length(); if(size>10_000_000) throw new IOException("Response too large. Try a shorter task.");
            if(line.startsWith("data:")) { if(data.length()>0) data.append('\n'); data.append(line.substring(5).trim()); }
            else if(line.isEmpty() && data.length()>0) {
                String raw=data.toString(); data.setLength(0); if(raw.equals("[DONE]")) continue;
                JSONObject event=new JSONObject(raw); String type=event.optString("type");
                JSONObject body=event.optJSONObject("response");
                if(type.equals("response.completed")) {
                    if(body==null || !"completed".equals(body.optString("status"))) throw new IOException("Response was incomplete. No further actions were run.");
                    return body;
                }
                if(type.equals("response.failed") || type.equals("response.incomplete") || type.equals("error")) {
                    JSONObject err=body==null?event.optJSONObject("error"):body.optJSONObject("error");
                    throw new IOException(error(err==null?event.optString("code"):err.optString("code"),0));
                }
            }
        }
        throw new IOException("Connection ended before completion. No further actions were run.");
    }
    public static String publicUrl(String text) throws Exception {
        URI u=new URI(text); String host=u.getHost();
        if(!Set.of("http","https").contains(u.getScheme()) || host==null || u.getUserInfo()!=null || u.getPort()!=-1 && u.getPort()!=80 && u.getPort()!=443) throw new IOException("Only public HTTP(S) pages are supported.");
        String h=host.toLowerCase(Locale.ROOT);
        if(h.equals("localhost") || h.endsWith(".local") || !h.contains(".") || h.contains(":") || h.matches("[0-9.]+")) throw new IOException("Local or numeric addresses are not supported.");
        return u.toASCIIString();
    }
    public static String toolName(JSONObject call) throws IOException {
        String name=call.optString("name"), namespace=call.optString("namespace");
        if(name.startsWith("assistant.")) name=name.substring(10);
        if(!namespace.isEmpty() && !namespace.equals("assistant")) throw new IOException("Unknown tool namespace");
        if(!Set.of("read_screen","click","type_text","scroll","open_url","launch_app","back").contains(name)) throw new IOException("Unknown tool");
        return name;
    }
}
