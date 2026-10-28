package com.arafat.assistant;

import android.content.*;
import android.net.Uri;
import org.json.*;
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.concurrent.atomic.AtomicBoolean;

final class AuthSession {
    private final Context context;
    private final SecureStore store;
    private volatile JSONObject record;
    private final SharedPreferences registration;
    AuthSession(Context c) throws Exception {
        context=c.getApplicationContext(); store=new SecureStore(context); record=store.load();
        registration=context.getSharedPreferences("chatgpt-registration",Context.MODE_PRIVATE);
        if(!registration.contains("host")) registration.edit().putString("host","urn:uuid:"+UUID.randomUUID()).commit();
    }
    String label() { return record.optString("email",record.has("access_token")?"ChatGPT account connected":"Not connected"); }
    boolean ready() { return record.has("access_token") && Protocol.plan(record); }
    synchronized void signIn(AtomicBoolean cancelled,Runnable opened) throws Exception {
        String client=record.optString("client_id",registration.getString("client",null));
        String state=Protocol.random(),nonce=Protocol.random(),verifier=Protocol.random();
        Map<String,String> callback=null;
        try(ServerSocket server=new ServerSocket(0,8,InetAddress.getByName("127.0.0.1"))) {
            server.setSoTimeout(500);
            String redirect="http://127.0.0.1:"+server.getLocalPort()+"/auth/callback";
            Map<String,String> p=new LinkedHashMap<>();
            p.put("client_id",client==null?"dynamic_agent_client":client); p.put("ext_agent_host_id",registration.getString("host",""));
            if(client==null) p.put("agent_name_hint","Arafat Assistant Android");
            if(record.has("id_token")) p.put("id_token_hint",record.getString("id_token"));
            if(record.has("email")) p.put("login_hint",record.getString("email"));
            p.put("response_type","code"); p.put("redirect_uri",redirect); p.put("scope",Protocol.SCOPE); p.put("resource",Protocol.RESOURCE);
            p.put("state",state); p.put("nonce",nonce); p.put("code_challenge_method","S256"); p.put("code_challenge",Protocol.challenge(verifier));
            Intent intent=new Intent(Intent.ACTION_VIEW,Uri.parse(Protocol.ISSUER+"/api/accounts/authorize?"+Protocol.form(p))).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            context.startActivity(intent); opened.run(); long deadline=System.currentTimeMillis()+300000;
            while(callback==null && System.currentTimeMillis()<deadline) {
                Protocol.check(cancelled);
                try(Socket socket=server.accept()) {
                    socket.setSoTimeout(2000);
                    BufferedReader in=new BufferedReader(new InputStreamReader(socket.getInputStream(),StandardCharsets.US_ASCII));
                    StringBuilder first=new StringBuilder(); int ch;
                    while(first.length()<17000 && (ch=in.read())!=-1 && ch!='\n') first.append((char)ch);
                    boolean valid=false;
                    try { String[] req=first.toString().trim().split(" "); if(req.length==3 && req[0].equals("GET")) { callback=Protocol.callback(req[1],state,client); valid=true; } } catch(IOException ignored) {}
                    String message=valid?"Sign-in received. Return to Arafat Assistant to finish connecting.":"This sign-in callback could not be verified. Return to the original sign-in tab.";
                    byte[] body=message.getBytes(StandardCharsets.UTF_8);
                    String headers="HTTP/1.1 "+(valid?"200 OK":"400 Bad Request")+"\r\nContent-Type: text/plain; charset=utf-8\r\nCache-Control: no-store\r\nReferrer-Policy: no-referrer\r\nConnection: close\r\nContent-Length: "+body.length+"\r\n\r\n";
                    socket.getOutputStream().write(headers.getBytes(StandardCharsets.US_ASCII)); socket.getOutputStream().write(body);
                } catch(SocketTimeoutException ignored) {}
            }
            if(callback==null) throw new IOException("Sign-in timed out. Return to the app and try again.");
            Protocol.check(cancelled);
            String issued=callback.get("client_id"); registration.edit().putString("client",issued).commit();
            JSONObject data=Http.json(Protocol.ISSUER+"/api/accounts/oauth/token",null,Protocol.form(Map.of("grant_type","authorization_code","client_id",issued,"code",callback.get("code"),"code_verifier",verifier,"redirect_uri",redirect,"resource",Protocol.RESOURCE)));
            JSONObject claims=Protocol.verify(data.getString("id_token"),issued,nonce,record.optString("sub",null),Http.json(Protocol.ISSUER+"/.well-known/jwks.json",null,null),System.currentTimeMillis()/1000);
            JSONObject updated=tokenRecord(data,issued,claims,record); Protocol.check(cancelled); store.save(updated); record=updated;
        }
    }
    static JSONObject tokenRecord(JSONObject data,String client,JSONObject claims,JSONObject old) throws Exception {
        long duration=data.getLong("expires_in"); String access=data.getString("access_token");
        if(duration<=0 || duration>31536000 || access.isEmpty() || !data.optString("token_type","Bearer").equalsIgnoreCase("Bearer")) throw new IOException("Incomplete ChatGPT connection. Sign in again.");
        return new JSONObject().put("client_id",client).put("sub",claims.getString("sub"))
            .put("email",claims.optString("email",old.optString("email",""))).put("access_token",access)
            .put("refresh_token",data.optString("refresh_token",old.optString("refresh_token","")))
            .put("id_token",data.optString("id_token",old.optString("id_token","")))
            .put("scope",data.optString("scope",old.optString("scope","")))
            .put("expires_at",System.currentTimeMillis()/1000+duration).put("earliest_refresh_at",data.optLong("earliest_refresh_at",0));
    }
    synchronized String token() throws Exception {
        if(!ready()) throw new IOException("Select Continue with ChatGPT and allow Use your ChatGPT plan first.");
        long now=System.currentTimeMillis()/1000;
        if(record.getLong("expires_at")>now+60) return record.getString("access_token");
        if(now<record.optLong("earliest_refresh_at")) {
            if(now<record.getLong("expires_at")) return record.getString("access_token");
            throw new IOException("ChatGPT renewal is not available yet. Try again later.");
        }
        if(record.optString("refresh_token").isEmpty()) throw new IOException("Your connection expired. Sign in again.");
        JSONObject data=Http.json(Protocol.ISSUER+"/api/accounts/oauth/token",null,Protocol.form(Map.of("grant_type","refresh_token","client_id",record.getString("client_id"),"refresh_token",record.getString("refresh_token"),"resource",Protocol.RESOURCE)));
        JSONObject claims=new JSONObject().put("sub",record.getString("sub")).put("email",record.optString("email"));
        if(data.has("id_token")) claims=Protocol.verify(data.getString("id_token"),record.getString("client_id"),null,record.getString("sub"),Http.json(Protocol.ISSUER+"/.well-known/jwks.json",null,null),now);
        JSONObject renewed=tokenRecord(data,record.getString("client_id"),claims,record); store.save(renewed); record=renewed;
        if(!Protocol.plan(record)) throw new IOException("ChatGPT plan access was removed. Sign in again.");
        return record.getString("access_token");
    }
    synchronized JSONArray models() throws Exception {
        JSONArray raw=Http.json(Protocol.RESOURCE+"/models",token(),null).optJSONArray("models"), result=new JSONArray();
        if(raw!=null) for(int i=0;i<raw.length();i++) { JSONObject m=raw.getJSONObject(i); if(m.optString("visibility").equals("list") && !m.optString("slug").isEmpty()) result.put(m); }
        if(result.length()==0) throw new IOException("No models available for this account. Check eligibility and plan permission.");
        return result;
    }
    synchronized boolean signOut() {
        boolean revoked=!record.has("refresh_token");
        try {
            String endpoint=Http.json(Protocol.ISSUER+"/.well-known/openid-configuration",null,null).getString("revocation_endpoint");
            if(!endpoint.startsWith(Protocol.ISSUER+"/")) throw new IOException("Invalid revocation address");
            HttpURLConnection c=Http.open(endpoint,null,Protocol.form(Map.of("token",record.getString("refresh_token"),"token_type_hint","refresh_token","client_id",record.getString("client_id"))),"application/x-www-form-urlencoded");
            try { revoked=c.getResponseCode()==200; } finally { c.disconnect(); }
        } catch(Exception ignored) {}
        String id=record.optString("client_id",registration.getString("client",null));
        if(id!=null) registration.edit().putString("client",id).commit();
        store.clear(); record=new JSONObject(); return revoked;
    }
}
