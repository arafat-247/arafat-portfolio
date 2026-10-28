package com.arafat.assistant;

import android.content.Context;
import android.os.*;
import org.json.*;
import java.lang.ref.WeakReference;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicBoolean;

final class AppState {
    static AppState singleton;
    static synchronized AppState get(Context c) { if(singleton==null) singleton=new AppState(c); return singleton; }
    final Handler main=new Handler(Looper.getMainLooper());
    final ExecutorService worker=Executors.newSingleThreadExecutor();
    final List<String> messages=new ArrayList<>();
    volatile AuthSession auth;
    volatile boolean busy;
    volatile JSONArray models=new JSONArray();
    volatile AtomicBoolean cancelled=new AtomicBoolean();
    volatile PlanClient client;
    private WeakReference<MainActivity> activity=new WeakReference<>(null);
    private AppState(Context c) {
        busy=true;
        worker.execute(()->{
            try { auth=new AuthSession(c); } catch(Exception e) { post("The saved connection could not be opened. Use Reset local connection, then sign in again."); }
            main.post(()->{ busy=false; refresh(); });
        });
    }
    void attach(MainActivity a) { activity=new WeakReference<>(a); refresh(); }
    void detach(MainActivity a) { if(activity.get()==a) activity.clear(); }
    void refresh() { MainActivity a=activity.get(); if(a!=null) a.refresh(); }
    void post(String text) { main.post(()->{
        messages.add(text); while(messages.size()>40) messages.remove(0);
        refresh(); DeviceService s=DeviceService.instance; if(s!=null) s.update(text);
    }); }
    interface Work { void run() throws Exception; }
    boolean start(Work work) {
        if(busy) return false;
        busy=true; cancelled=new AtomicBoolean(); refresh();
        worker.execute(()->{
            try { work.run(); } catch(Exception e) { post(e instanceof java.io.IOException?e.getMessage():"The operation could not finish. Check your connection and try again."); }
            finally { client=null; main.post(()->{ busy=false; refresh(); }); }
        }); return true;
    }
    void signIn() { start(()->{
        if(auth==null) throw new java.io.IOException("Reset the local connection first.");
        auth.signIn(cancelled,()->post("In your browser, sign in and allow Use your ChatGPT plan. Then return to this app."));
        post(auth.ready()?"Connected. Usage comes from your existing ChatGPT allowance.":"Signed in, but plan access was not granted. Reconnect and allow Use your ChatGPT plan.");
        if(auth.ready()) models=auth.models();
    }); }
    void loadModels() { start(()->{ if(auth==null) throw new java.io.IOException("Sign in first."); models=auth.models(); post("Available models refreshed."); }); }
    void stop() { cancelled.set(true); PlanClient c=client; if(c!=null) workerCancel(c); DeviceService s=DeviceService.instance; if(s!=null) s.finish(); post("Stop requested. Completed actions cannot be undone."); }
    private void workerCancel(PlanClient c) { new Thread(c::cancel,"cancel-connection").start(); }
    void task(String instruction,String model,Set<String> packages,MainActivity owner) {
        boolean controls=!packages.isEmpty();
        DeviceService service=DeviceService.instance;
        if(controls && service==null) { post("Enable Arafat Assistant controls in Android Accessibility settings first."); return; }
        start(()->{
            post("You: "+instruction);
            client=new PlanClient(auth,model,cancelled);
            if(controls) {
                service.begin(packages,cancelled,this::stop);
                main.post(()->owner.moveTaskToBack(true));
                // The user may need to bring the desired app to the foreground.
                Thread.sleep(700);
            }
            try {
                Agent.run(instruction,String.join(", ",packages),controls,cancelled,client::response,controls?service::execute:null,this::post);
            } finally { if(controls) service.finish(); }
        });
    }
}
