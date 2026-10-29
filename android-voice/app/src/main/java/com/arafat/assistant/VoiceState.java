package com.arafat.assistant;

import android.content.Context;
import android.os.*;
import org.json.*;
import java.lang.ref.WeakReference;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicBoolean;

final class VoiceState {
    private static VoiceState singleton;
    static synchronized VoiceState get(Context c) { if(singleton==null) singleton=new VoiceState(c.getApplicationContext()); return singleton; }
    final Handler main=new Handler(Looper.getMainLooper());
    final ExecutorService worker=Executors.newSingleThreadExecutor();
    final List<String> messages=new ArrayList<>();
    final VoiceConversation conversation=new VoiceConversation();
    volatile AuthSession auth;
    volatile boolean busy;
    volatile JSONArray models=new JSONArray();
    volatile AtomicBoolean cancelled=new AtomicBoolean();
    volatile VoiceClient client;
    private String activeModel="";
    private WeakReference<VoiceActivity> activity=new WeakReference<>(null);
    private VoiceState(Context c) {
        busy=true;
        worker.execute(()->{
            try { auth=new AuthSession(c); } catch(Exception e) { post("The saved connection could not be opened. Use Reset local connection, then sign in again."); }
            main.post(()->{ busy=false; refresh(); });
        });
    }
    void attach(VoiceActivity a) { activity=new WeakReference<>(a); refresh(); }
    void detach(VoiceActivity a) { if(activity.get()==a) activity.clear(); }
    void refresh() { VoiceActivity a=activity.get(); if(a!=null) a.refresh(); }
    void post(String text) { main.post(()->{ messages.add(text); while(messages.size()>40) messages.remove(0); refresh(); }); }
    interface Work { void run() throws Exception; }
    boolean start(Work work) {
        if(busy) return false;
        busy=true; cancelled=new AtomicBoolean(); refresh();
        worker.execute(()->{
            try { work.run(); } catch(Exception e) { post(cancelled.get()?"Request stopped.":e instanceof java.io.IOException?e.getMessage():"The operation could not finish. Check your connection and try again."); }
            finally { client=null; main.post(()->{ busy=false; refresh(); }); }
        }); return true;
    }
    void signIn() { start(()->{
        if(auth==null) throw new java.io.IOException("Reset the local connection first.");
        auth.signIn(cancelled,()->post("In your browser, sign in and allow Use your ChatGPT plan if offered. Then return to Arafat Voice."));
        post(auth.ready()?"Connected. Existing ChatGPT plan limits apply.":"Signed in, but plan access was not granted. Availability depends on your account and workspace.");
        if(auth.ready()) models=auth.models();
    }); }
    void loadModels() { start(()->{ if(auth==null) throw new java.io.IOException("Sign in first."); models=auth.models(); post("Available models refreshed."); }); }
    void stop() { cancelled.set(true); VoiceClient c=client; if(c!=null) new Thread(c::cancel,"cancel-voice-request").start(); post("Stop requested."); }
    void clearConversation() { if(!busy) { conversation.clear(); messages.clear(); activeModel=""; refresh(); } }
    void task(String instruction,String model) { start(()->{
        if(!activeModel.equals(model)) { conversation.clear(); activeModel=model; }
        JSONArray input=conversation.input(instruction); post("You: "+instruction);
        client=new VoiceClient(auth,model,cancelled);
        String answer=client.response(input); Protocol.check(cancelled);
        conversation.commit(instruction,answer); post("Assistant: "+answer);
    }); }
}
