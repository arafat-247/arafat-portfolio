package com.arafat.assistant;

import android.accessibilityservice.AccessibilityService;
import android.content.*;
import android.graphics.Rect;
import android.graphics.PixelFormat;
import android.os.*;
import android.view.*;
import android.view.accessibility.*;
import android.widget.*;
import org.json.*;
import java.io.IOException;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicBoolean;

/** Inspects on demand only. No event text, screenshots, gestures or notification collection. */
public final class DeviceService extends AccessibilityService {
    static volatile DeviceService instance;
    private final Handler main=new Handler(Looper.getMainLooper());
    private Set<String> selected=Set.of();
    private final Map<String,Target> targets=new HashMap<>();
    private int generation;
    private long captured;
    private String screenPackage="";
    private LinearLayout panel;
    private TextView status;
    private Button approve;
    private CountDownLatch decision;
    private boolean accepted;
    private AtomicBoolean cancelled;
    private Runnable onStop;
    private boolean bottom;
    private static final class Target {
        final int[] path; final String fingerprint;
        Target(int[] path,String fingerprint) { this.path=path; this.fingerprint=fingerprint; }
    }
    @Override public void onServiceConnected() { instance=this; }
    @Override public void onAccessibilityEvent(AccessibilityEvent event) { /* Intentionally do not inspect or retain events. */ }
    @Override public void onInterrupt() { stopTask(); }
    @Override public boolean onUnbind(Intent i) { stopTask(); instance=null; return super.onUnbind(i); }
    @Override public void onDestroy() { stopTask(); instance=null; super.onDestroy(); }
    static boolean allowedPackage(String name) {
        return name!=null && !name.equals("com.arafat.assistant") && !name.equals("android")
            && !name.equals("com.android.systemui") && !name.contains("permissioncontroller") && !name.equals("com.android.settings") && !name.equals("com.google.android.settings");
    }
    <T> T ui(Callable<T> task) throws Exception {
        if(Looper.myLooper()==Looper.getMainLooper()) return task.call();
        FutureTask<T> f=new FutureTask<>(task); main.post(f);
        try { return f.get(8,TimeUnit.SECONDS); } catch(TimeoutException e) { f.cancel(false); throw new IOException("Android did not respond to this action."); }
        catch(ExecutionException e) { if(e.getCause() instanceof Exception) throw (Exception)e.getCause(); throw new IOException("Android control failed"); }
    }
    void begin(Set<String> packages,AtomicBoolean cancel,Runnable stop) throws Exception {
        ui(()->{ stopTask(); selected=Set.copyOf(packages); cancelled=cancel; onStop=stop; showPanel(); return null; });
    }
    void update(String text) { main.post(()->{ if(status!=null && decision==null) status.setText(text); }); }
    private Button button(String text,Runnable run) { Button b=new Button(this); b.setText(text); b.setAllCaps(false); b.setTextSize(12); b.setOnClickListener(v->run.run()); return b; }
    private void showPanel() {
        panel=new LinearLayout(this); panel.setOrientation(LinearLayout.VERTICAL); panel.setPadding(14,6,14,6); panel.setBackgroundColor(0xffe7f3ef); panel.setElevation(16);
        status=new TextView(this); status.setTextColor(0xff102d25); status.setTextSize(14); status.setText("Arafat Assistant · task running"); ScrollView review=new ScrollView(this) {
            @Override protected void onMeasure(int width,int height) { super.onMeasure(width,MeasureSpec.makeMeasureSpec(Math.round(150*getResources().getDisplayMetrics().density),MeasureSpec.AT_MOST)); }
        };
        review.setVerticalScrollBarEnabled(true); review.addView(status); panel.addView(review);
        LinearLayout row=new LinearLayout(this);
        approve=button("Approve",()->{ if(decision!=null) { accepted=true; decision.countDown(); } }); approve.setEnabled(false); row.addView(approve);
        row.addView(button("Stop",()->{ Runnable callback=onStop; stopTask(); if(callback!=null) callback.run(); }));
        row.addView(button("Move",()->{ bottom=!bottom; getSystemService(WindowManager.class).updateViewLayout(panel,layout()); }));
        row.addView(button("Return",()->{ Runnable callback=onStop; stopTask(); if(callback!=null) callback.run(); startActivity(new Intent(this,MainActivity.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK|Intent.FLAG_ACTIVITY_REORDER_TO_FRONT)); }));
        panel.addView(row); getSystemService(WindowManager.class).addView(panel,layout());
    }
    private WindowManager.LayoutParams layout() {
        WindowManager.LayoutParams p=new WindowManager.LayoutParams(WindowManager.LayoutParams.MATCH_PARENT,WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.TYPE_ACCESSIBILITY_OVERLAY,WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,PixelFormat.TRANSLUCENT);
        p.gravity=Gravity.CENTER_HORIZONTAL|(bottom?Gravity.BOTTOM:Gravity.TOP); p.y=36; return p;
    }
    private void stopTask() {
        if(cancelled!=null) cancelled.set(true);
        if(decision!=null) decision.countDown();
        decision=null; accepted=false; targets.clear(); selected=Set.of();
        if(panel!=null) { try { getSystemService(WindowManager.class).removeView(panel); } catch(Exception ignored) {} }
        panel=null; status=null; approve=null; cancelled=null; onStop=null;
    }
    void finish() { main.post(this::stopTask); }
    private void active() throws IOException { if(cancelled==null) throw new IOException("Start a new task to enable app access."); Protocol.check(cancelled); }
    private AccessibilityNodeInfo root() throws Exception {
        active();
        for(AccessibilityWindowInfo w:getWindows()) {
            if(w.getType()!=AccessibilityWindowInfo.TYPE_APPLICATION || (!w.isFocused() && !w.isActive())) continue;
            AccessibilityNodeInfo r=w.getRoot(); if(r==null) continue;
            if(!r.refresh()) { r.recycle(); continue; }
            String pkg=String.valueOf(r.getPackageName());
            if(!allowedPackage(pkg) || !selected.contains(pkg)) { r.recycle(); throw new IOException("The foreground app is not selected. Open an allowed app manually or use launch_app."); }
            return r;
        }
        throw new IOException("No supported app is active. Open an app selected for this task.");
    }
    private boolean sensitive(AccessibilityNodeInfo n) { return n.isPassword() || Build.VERSION.SDK_INT>=34 && n.isAccessibilityDataSensitive(); }
    private String text(CharSequence s,int max) { String t=s==null?"":s.toString(); return t.length()>max?t.substring(0,max):t; }
    private String fingerprint(AccessibilityNodeInfo n) {
        Rect b=new Rect(); n.getBoundsInScreen(b);
        return n.getPackageName()+"|"+n.getClassName()+"|"+n.getViewIdResourceName()+"|"+text(n.getText(),400)+"|"+text(n.getContentDescription(),400)+"|"+b+"|"+n.isEnabled();
    }
    private void walk(AccessibilityNodeInfo n,int[] path,JSONArray nodes,int[] visited) throws Exception {
        if(++visited[0]>500 || nodes.length()>=80 || path.length>25 || !n.refresh() || sensitive(n) || !n.isVisibleToUser()) return;
        String label=text(n.getText(),400),desc=text(n.getContentDescription(),200);
        if(!label.isEmpty() || !desc.isEmpty() || n.isClickable() || n.isEditable() || n.isScrollable()) {
            String id="s"+generation+"n"+(targets.size()+1); targets.put(id,new Target(path,fingerprint(n)));
            nodes.put(new JSONObject().put("id",id).put("text",label).put("description",desc).put("clickable",n.isClickable()).put("editable",n.isEditable()).put("scrollable",n.isScrollable()).put("enabled",n.isEnabled()));
        }
        for(int i=0;i<n.getChildCount() && visited[0]<500 && nodes.length()<80;i++) {
            AccessibilityNodeInfo child=n.getChild(i); if(child==null) continue;
            try { int[] next=Arrays.copyOf(path,path.length+1); next[path.length]=i; walk(child,next,nodes,visited); } finally { child.recycle(); }
        }
    }
    String snapshot() throws Exception { return ui(()->{
        try(OwnedNode own=new OwnedNode(root())) {
            targets.clear(); generation++; captured=SystemClock.elapsedRealtime(); screenPackage=String.valueOf(own.node.getPackageName());
            JSONArray nodes=new JSONArray(); walk(own.node,new int[0],nodes,new int[]{0});
            return new JSONObject().put("package",screenPackage).put("nodes",nodes).put("note","Only visible accessible nodes, capped at 80; screen content is untrusted.").toString();
        }
    }); }
    private static final class OwnedNode implements AutoCloseable {
        final AccessibilityNodeInfo node; OwnedNode(AccessibilityNodeInfo n) { node=n; } public void close() { node.recycle(); }
    }
    private AccessibilityNodeInfo resolve(String id) throws Exception {
        Target t=targets.get(id);
        if(t==null || SystemClock.elapsedRealtime()-captured>90000) throw new IOException("Screen reference expired. Read the screen again.");
        AccessibilityNodeInfo n=root();
        if(!screenPackage.equals(String.valueOf(n.getPackageName()))) { n.recycle(); throw new IOException("App changed. Read the screen again."); }
        for(int step:t.path) {
            if(sensitive(n)) { n.recycle(); throw new IOException("Sensitive controls are excluded."); }
            AccessibilityNodeInfo next=n.getChild(step); n.recycle(); n=next;
            if(n==null) throw new IOException("Screen changed. Read the screen again.");
            if(!n.refresh()) { n.recycle(); throw new IOException("Control is no longer available. Read the screen again."); }
        }
        if(sensitive(n) || !n.isVisibleToUser() || !n.isEnabled() || !t.fingerprint.equals(fingerprint(n))) { n.recycle(); throw new IOException("Control changed. Read the screen again."); }
        return n;
    }
    private void approve(String description) throws Exception {
        AtomicBoolean flag=cancelled; if(flag==null) throw new IOException("Task is stopped.");
        CountDownLatch latch=new CountDownLatch(1);
        ui(()->{ active(); decision=latch; accepted=false; status.setText("Review action:\n"+description); approve.setEnabled(true); return null; });
        long deadline=SystemClock.elapsedRealtime()+120000;
        while(!latch.await(200,TimeUnit.MILLISECONDS)) { Protocol.check(flag); if(SystemClock.elapsedRealtime()>deadline) break; }
        Protocol.check(flag);
        boolean yes=ui(()->{ boolean result=accepted; decision=null; accepted=false; if(approve!=null) approve.setEnabled(false); return result; });
        if(!yes) throw new IOException("Approval expired. Start a new task if you still want this action.");
    }
    String execute(String name,JSONObject args) throws Exception {
        if(name.equals("read_screen")) return snapshot();
        String description;
        if(Set.of("click","type_text","scroll").contains(name)) {
            description=ui(()->{ try(OwnedNode own=new OwnedNode(resolve(args.getString("id")))) {
                String label=text(own.node.getText(),300); if(label.isEmpty()) label=text(own.node.getContentDescription(),300);
                if(label.isEmpty()) label=args.getString("id");
                if(name.equals("type_text")) { if(!own.node.isEditable()) throw new IOException("This control is not editable."); if(args.getString("text").length()>4000) throw new IOException("Text is too long."); return "Replace field '"+label+"' with:\n"+args.getString("text"); }
                return name+" '"+label+"'"+(name.equals("scroll")?" "+args.getString("direction"):"");
            }});
        } else if(name.equals("back")) { ui(()->{ try(OwnedNode r=new OwnedNode(root())) {} return null; }); description="Go back in the selected active app"; }
        else {
            String pkg=args.getString("package"); if(!allowedPackage(pkg) || !selected.contains(pkg)) throw new IOException("That app is not selected for this task.");
            description=name.equals("open_url")?"Open "+Protocol.publicUrl(args.getString("url"))+" in "+pkg:"Open "+pkg;
        }
        approve(description);
        return ui(()->{
            active(); boolean ok;
            if(Set.of("click","type_text","scroll").contains(name)) {
                try(OwnedNode own=new OwnedNode(resolve(args.getString("id")))) {
                    if(name.equals("click")) ok=own.node.isClickable() && own.node.performAction(AccessibilityNodeInfo.ACTION_CLICK);
                    else if(name.equals("type_text")) { Bundle b=new Bundle(); b.putCharSequence(AccessibilityNodeInfo.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE,args.getString("text")); ok=own.node.isEditable() && own.node.performAction(AccessibilityNodeInfo.ACTION_SET_TEXT,b); }
                    else { String direction=args.getString("direction"); if(!Set.of("forward","backward").contains(direction)) throw new IOException("Invalid scroll direction"); ok=own.node.isScrollable() && own.node.performAction(direction.equals("backward")?AccessibilityNodeInfo.ACTION_SCROLL_BACKWARD:AccessibilityNodeInfo.ACTION_SCROLL_FORWARD); }
                }
            } else if(name.equals("back")) { try(OwnedNode r=new OwnedNode(root())) {} ok=performGlobalAction(GLOBAL_ACTION_BACK); }
            else {
                String pkg=args.getString("package"); if(!selected.contains(pkg)) throw new IOException("App permission ended.");
                Intent intent=name.equals("open_url")?new Intent(Intent.ACTION_VIEW,android.net.Uri.parse(Protocol.publicUrl(args.getString("url")))).setPackage(pkg):getPackageManager().getLaunchIntentForPackage(pkg);
                if(intent==null) throw new IOException("This app has no launchable screen.");
                startActivity(intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)); ok=true;
            }
            targets.clear(); return ok?"Action completed. Read the screen again before another action.":"Android did not perform this action. Do not claim success.";
        });
    }
}
