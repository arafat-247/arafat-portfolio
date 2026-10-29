package com.arafat.assistant;

import org.json.*;
import java.io.IOException;

/** Keep complete user/reply pairs, and never retain a failed or stopped request. */
final class VoiceConversation {
    private JSONArray history=new JSONArray();
    synchronized void clear() { history=new JSONArray(); }
    synchronized JSONArray input(String instruction) throws Exception {
        if(history.toString().length()+instruction.length()>48000) throw new IOException("This conversation is full. Start a new conversation and include the context you need.");
        return new JSONArray(history.toString()).put(new JSONObject().put("role","user").put("content",instruction));
    }
    synchronized void commit(String instruction,String reply) throws Exception {
        history.put(new JSONObject().put("role","user").put("content",instruction));
        history.put(new JSONObject().put("role","assistant").put("content",reply));
        while(history.length()>16) { history.remove(0); history.remove(0); }
    }
}
