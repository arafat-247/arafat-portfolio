package com.arafat.assistant;

import org.junit.Test;
import static org.junit.Assert.*;
import org.json.*;
import java.io.*;
import java.security.*;
import java.security.interfaces.RSAPublicKey;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.concurrent.atomic.AtomicBoolean;

public class ProtocolTest {
    @Test public void pkceUsesRfcVector() throws Exception {
        assertEquals("E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM",Protocol.challenge("dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"));
        assertNotEquals(Protocol.random(),Protocol.random());
    }
    @Test public void callbacksRejectDuplicatesStateAndAccountChanges() throws Exception {
        assertEquals("oaiapp_test",Protocol.callback("/auth/callback?state=s&code=c&client_id=oaiapp_test","s",null).get("client_id"));
        assertEquals("oaiapp_test",Protocol.callback("/auth/callback?state=s&code=c","s","oaiapp_test").get("client_id"));
        for(String target:List.of("/callback?state=s&code=c&client_id=oaiapp_test","/auth/callback?state=x&code=c&client_id=oaiapp_test","/auth/callback?state=s&state=s&code=c&client_id=oaiapp_test","/auth/callback?state=s&code=c&client_id=dynamic_agent_client","/auth/callback?state=s&error=access_denied","https://evil.test/auth/callback?state=s&code=c&client_id=oaiapp_test")) {
            assertThrows(Exception.class,()->Protocol.callback(target,"s",null));
        }
        assertThrows(Exception.class,()->Protocol.callback("/auth/callback?state=s&code=c&client_id=oaiapp_other","s","oaiapp_test"));
        assertThrows(Protocol.Declined.class,()->Protocol.callback("/auth/callback?state=s&error=access_denied","s",null));
    }
    @Test public void identitySignatureAndClaimsAreVerified() throws Exception {
        KeyPairGenerator gen=KeyPairGenerator.getInstance("RSA"); gen.initialize(2048); KeyPair pair=gen.generateKeyPair(); RSAPublicKey key=(RSAPublicKey)pair.getPublic();
        JSONObject jwk=new JSONObject().put("kid","test").put("kty","RSA").put("n",Protocol.b64(unsigned(key.getModulus().toByteArray()))).put("e",Protocol.b64(unsigned(key.getPublicExponent().toByteArray())));
        JSONObject keys=new JSONObject().put("keys",new JSONArray().put(jwk));
        JSONObject claims=new JSONObject().put("iss",Protocol.ISSUER).put("aud","oaiapp_test").put("sub","user").put("exp",2000).put("iat",900).put("nonce","n");
        String encoded=sign(pair,claims,"RS256");
        assertEquals("user",Protocol.verify(encoded,"oaiapp_test","n",null,keys,1000).getString("sub"));
        assertThrows(Exception.class,()->Protocol.verify(encoded,"oaiapp_wrong","n",null,keys,1000));
        assertThrows(Exception.class,()->Protocol.verify(encoded,"oaiapp_test","bad",null,keys,1000));
        assertThrows(Exception.class,()->Protocol.verify(encoded,"oaiapp_test","n","other",keys,1000));
        assertThrows(Exception.class,()->Protocol.verify(encoded,"oaiapp_test","n",null,keys,3000));
        assertThrows(Exception.class,()->Protocol.verify(sign(pair,claims,"none"),"oaiapp_test","n",null,keys,1000));
        String[] parts=encoded.split("\\."); parts[1]=Protocol.b64(claims.put("sub","attacker").toString().getBytes(StandardCharsets.UTF_8));
        assertThrows(Exception.class,()->Protocol.verify(String.join(".",parts),"oaiapp_test","n",null,keys,1000));
    }
    private byte[] unsigned(byte[] n) { return n[0]==0?Arrays.copyOfRange(n,1,n.length):n; }
    private String sign(KeyPair pair,JSONObject claims,String alg) throws Exception {
        String content=Protocol.b64(new JSONObject().put("alg",alg).put("kid","test").toString().getBytes(StandardCharsets.UTF_8))+"."+Protocol.b64(claims.toString().getBytes(StandardCharsets.UTF_8));
        Signature s=Signature.getInstance("SHA256withRSA"); s.initSign(pair.getPrivate()); s.update(content.getBytes(StandardCharsets.US_ASCII)); return content+"."+Protocol.b64(s.sign());
    }
    @Test public void bothPlanScopesRequired() throws Exception {
        assertFalse(Protocol.plan(new JSONObject().put("scope","openid profile email")));
        assertFalse(Protocol.plan(new JSONObject().put("scope","chatgpt.tokens.use.direct")));
        assertTrue(Protocol.plan(new JSONObject().put("scope",Protocol.SCOPE)));
    }
    @Test public void partialStreamCannotRunActions() throws Exception {
        String delta="data: {\"type\":\"response.output_text.delta\",\"delta\":\"hello\"}\n\n";
        assertThrows(Exception.class,()->Protocol.completed(new StringReader(delta),new AtomicBoolean()));
        assertThrows(Exception.class,()->Protocol.completed(new StringReader("data: {\"type\":\"response.incomplete\"}\n\n"),new AtomicBoolean()));
        String success="data: {\"type\":\"response.completed\",\"response\":{\"status\":\"completed\",\"output\":[]}}\n\n";
        assertEquals("completed",Protocol.completed(new StringReader(delta+success),new AtomicBoolean()).getString("status"));
        assertThrows(Exception.class,()->Protocol.completed(new StringReader(success),new AtomicBoolean(true)));
    }
    @Test public void planPayloadUsesSupportedPublicContract() throws Exception {
        JSONObject p=PlanClient.payload("selected-model",new JSONArray().put(new JSONObject().put("role","user").put("content","বাংলায় উত্তর দাও।")),true);
        assertFalse(p.getBoolean("store")); assertTrue(p.getBoolean("stream")); assertFalse(p.has("max_output_tokens")); assertFalse(p.has("temperature"));
        assertEquals("namespace",p.getJSONArray("tools").getJSONObject(0).getString("type"));
        assertEquals("assistant",p.getJSONArray("tools").getJSONObject(0).getString("name"));
        assertFalse(PlanClient.payload("model",new JSONArray(),false).has("tools"));
    }
    @Test public void onlyKnownToolsAndNamespacesAccepted() throws Exception {
        assertEquals("click",Protocol.toolName(new JSONObject().put("name","assistant.click")));
        assertThrows(Exception.class,()->Protocol.toolName(new JSONObject().put("name","shell")));
        assertThrows(Exception.class,()->Protocol.toolName(new JSONObject().put("name","click").put("namespace","evil")));
    }
    @Test public void urlsCannotOpenLocalFilesOrIntents() throws Exception {
        assertEquals("https://example.com/",Protocol.publicUrl("https://example.com/"));
        for(String url:List.of("file:///data/data/secret","intent://secret","javascript:alert(1)","http://localhost/","http://127.0.0.1/","http://192.168.1.1/","https://user:pass@example.com/","https://example.com:8000/","http://[::1]/")) assertThrows(Exception.class,()->Protocol.publicUrl(url));
    }
    @Test public void agentNeverExecutesWithControlsOffOrAfterCancellation() throws Exception {
        JSONObject call=new JSONObject().put("type","function_call").put("name","click").put("call_id","c").put("arguments","{\"id\":\"s1n1\"}");
        JSONObject response=new JSONObject().put("output",new JSONArray().put(call));
        AtomicBoolean invoked=new AtomicBoolean();
        assertThrows(Exception.class,()->Agent.run("task","",false,new AtomicBoolean(),(i,c)->response,(n,a)->{ invoked.set(true); return "done"; },t->{})); assertFalse(invoked.get());
        assertThrows(Exception.class,()->Agent.run("task","app",true,new AtomicBoolean(true),(i,c)->response,(n,a)->{ invoked.set(true); return "done"; },t->{})); assertFalse(invoked.get());
    }
    @Test public void toolResultsAndUnicodeSurviveTheNextTurn() throws Exception {
        int[] turn={0}; List<String> replies=new ArrayList<>();
        Agent.run("বাংলায় বলো","test.app",true,new AtomicBoolean(),(items,controls)->{
            if(turn[0]++==0) return new JSONObject().put("output",new JSONArray().put(new JSONObject().put("type","function_call").put("name","read_screen").put("namespace","assistant").put("call_id","c").put("arguments","{}")));
            assertEquals("বাংলা ফল",items.getJSONObject(items.length()-1).getString("output"));
            return new JSONObject().put("output",new JSONArray().put(new JSONObject().put("type","message").put("role","assistant").put("content",new JSONArray().put(new JSONObject().put("type","output_text").put("text","সফল")))));
        },(n,a)->"বাংলা ফল",replies::add);
        assertEquals(List.of("সফল"),replies); assertEquals(2,turn[0]);
    }
}
