package com.arafat.assistant;

import org.junit.Test;
import static org.junit.Assert.*;
import org.json.*;
import java.io.StringReader;
import java.util.concurrent.atomic.AtomicBoolean;

public class VoiceTest {
    private JSONObject message(String type,String value) throws Exception { return new JSONObject().put("type","message").put("content",new JSONArray().put(new JSONObject().put("type",type).put(type.equals("refusal")?"refusal":"text",value))); }
    @Test public void noToolsOrPaidFallbackFieldsAreSent() throws Exception {
        JSONObject payload=VoiceClient.payload("account-model",new VoiceConversation().input("বাংলায় বলো"));
        assertEquals("account-model",payload.getString("model")); assertFalse(payload.getBoolean("store")); assertTrue(payload.getBoolean("stream"));
        assertFalse(payload.has("tools")); assertFalse(payload.has("previous_response_id")); assertFalse(payload.has("max_output_tokens"));
        assertTrue(payload.getString("instructions").contains("no tools"));
    }
    @Test public void unexpectedToolCallRejectsTheWholeReply() throws Exception {
        JSONObject response=new JSONObject().put("output",new JSONArray().put(message("output_text","Some text")).put(new JSONObject().put("type","function_call").put("name","click")));
        assertThrows(Exception.class,()->VoiceClient.reply(response));
        assertThrows(Exception.class,()->VoiceClient.reply(new JSONObject().put("output",new JSONArray())));
    }
    @Test public void completedTextAndRefusalsAreVisibleButPartialStreamsFail() throws Exception {
        JSONObject response=new JSONObject().put("status","completed").put("output",new JSONArray().put(message("output_text","বাংলা উত্তর")));
        String stream="data: "+new JSONObject().put("type","response.completed").put("response",response)+"\n\n";
        assertEquals("বাংলা উত্তর",VoiceClient.reply(Protocol.completed(new StringReader(stream),new AtomicBoolean())));
        assertEquals("I cannot help with that.",VoiceClient.reply(new JSONObject().put("output",new JSONArray().put(message("refusal","I cannot help with that.")))));
        assertThrows(Exception.class,()->Protocol.completed(new StringReader("data: {\"type\":\"response.output_text.delta\",\"delta\":\"partial\"}\n\n"),new AtomicBoolean()));
        assertThrows(Exception.class,()->Protocol.completed(new StringReader(stream),new AtomicBoolean(true)));
    }
    @Test public void historyKeepsWholePairsAndOnlyCommittedReplies() throws Exception {
        VoiceConversation c=new VoiceConversation();
        c.input("failed draft"); assertEquals(1,c.input("new draft").length());
        for(int i=0;i<10;i++) c.commit("user "+i,"reply "+i);
        JSONArray input=c.input("next"); assertEquals(17,input.length()); assertEquals("user 2",input.getJSONObject(0).getString("content")); assertEquals("reply 9",input.getJSONObject(15).getString("content"));
        input.getJSONObject(0).put("content","mutated"); assertEquals("user 2",c.input("next").getJSONObject(0).getString("content"));
        c.clear(); assertEquals(1,c.input("বাংলা").length());
        assertThrows(Exception.class,()->c.input("x".repeat(48001)));
    }
}
