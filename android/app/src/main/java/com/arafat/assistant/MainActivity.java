package com.arafat.assistant;

import android.app.*;
import android.content.*;
import android.content.pm.ResolveInfo;
import android.graphics.Typeface;
import android.net.Uri;
import android.os.*;
import android.provider.Settings;
import android.speech.RecognizerIntent;
import android.view.*;
import android.widget.*;
import org.json.*;
import java.util.*;

public final class MainActivity extends Activity {
    private AppState state;
    private LinearLayout page;
    private EditText instruction;
    private TextView account,log,selectedLabel;
    private Spinner models,languages;
    private CheckBox share,offline;
    private Button signIn,run,voice,refreshModels,choose,disconnect,reset;
    private final Set<String> selected=new HashSet<>();
    private final List<String> slugs=new ArrayList<>();
    private String modelSignature="";
    private static final int VOICE=42;
    @Override public void onCreate(Bundle saved) {
        super.onCreate(saved); state=AppState.get(this);
        ScrollView scroll=new ScrollView(this); scroll.setFillViewport(true); scroll.setBackgroundColor(0xfff3f7f5);
        scroll.setOnApplyWindowInsetsListener((v,insets)->{ v.setPadding(insets.getSystemWindowInsetLeft(),insets.getSystemWindowInsetTop(),insets.getSystemWindowInsetRight(),insets.getSystemWindowInsetBottom()); return insets; });
        page=new LinearLayout(this); page.setOrientation(LinearLayout.VERTICAL); page.setPadding(dp(20),dp(20),dp(20),dp(28)); scroll.addView(page); setContentView(scroll);
        text("ARAFAT ASSISTANT",12,true); text("Your instructions. Your phone.",27,true);
        text("Android preview · English · বাংলা · other supported languages",14,false);
        account=text("Preparing local connection…",14,true);
        signIn=button("Continue with ChatGPT",()->state.signIn());
        LinearLayout authRow=new LinearLayout(this); page.addView(authRow);
        refreshModels=smallButton(authRow,"Refresh models",()->state.loadModels());
        smallButton(authRow,"Manage usage",()->open("https://chatgpt.com/settings/usage"));
        disconnect=smallButton(authRow,"Sign out",()->state.start(()->{
            boolean revoked=state.auth!=null && state.auth.signOut(); state.models=new JSONArray();
            state.post(revoked?"Signed out.":"Local credentials removed. Remote revocation was not confirmed. Disconnect this app in ChatGPT settings.");
        }));
        text("Uses an eligible ChatGPT plan and its existing limits. No API key, extra API billing or automatic paid fallback. This app does not import ChatGPT conversations.",13,false);
        text("Model",14,true); models=new Spinner(this); page.addView(models);
        text("Your instruction / আপনার নির্দেশ",17,true);
        instruction=new EditText(this); instruction.setHint("বাংলায় উত্তর দাও। / Give me a task…"); instruction.setMinLines(3); instruction.setMaxLines(8); instruction.setGravity(Gravity.TOP); instruction.setInputType(android.text.InputType.TYPE_CLASS_TEXT|android.text.InputType.TYPE_TEXT_FLAG_MULTI_LINE|android.text.InputType.TYPE_TEXT_FLAG_CAP_SENTENCES); page.addView(instruction);
        if(saved!=null) instruction.setText(saved.getString("draft",""));
        languages=new Spinner(this); languages.setAdapter(new ArrayAdapter<>(this,android.R.layout.simple_spinner_dropdown_item,new String[]{"English","বাংলা (বাংলাদেশ)","বাংলা (ভারত)","Phone language"})); page.addView(languages);
        offline=new CheckBox(this); offline.setText("Prefer offline voice recognition, if available"); offline.setChecked(true); page.addView(offline);
        voice=button("Dictate instruction",this::voice);
        text("Voice opens your phone’s speech service. Language support and offline availability depend on that service; it may process audio online. Review the transcript before Run. No always-on listening.",13,false);
        text("App controls",19,true);
        button("Open Android Accessibility settings",()->new AlertDialog.Builder(this).setTitle("Enable app controls only if you want them")
            .setMessage("During a task, Arafat Assistant can read visible accessible text in apps you select and send that text to OpenAI. Proposed taps, typing and scrolling need your approval. It does not inspect screen content while idle. You can stop a task or disable the service at any time. Password and marked sensitive controls are excluded; other sensitive content may still be visible. Do not select confidential apps.")
            .setPositiveButton("Open settings",(d,w)->startActivity(new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS))).setNegativeButton("Cancel",null).show());
        choose=button("Choose apps for this task",this::chooseApps);
        selectedLabel=text("No apps selected. Chat works without app access.",13,false);
        share=new CheckBox(this); share.setText("For this task, allow selected apps’ visible text to be shared with OpenAI and propose app actions"); page.addView(share);
        text("For websites, select your browser. Start with a public page. Handle sign-ins, passwords, permissions and sensitive actions yourself. Support depends on accessible controls exposed by each app.",13,false);
        run=button("Run instruction",this::run);
        button("Stop task",()->state.stop());
        text("Activity and replies",18,true); log=text("Ready. Connect ChatGPT, then try: বাংলায় উত্তর দাও।",15,false); log.setTextIsSelectable(true);
        button("Clear conversation",()->{ if(!state.busy) { state.messages.clear(); refresh(); } });
        reset=button("Reset local connection",()->{
            if(state.busy) return;
            new AlertDialog.Builder(this).setTitle("Remove this phone’s saved connection?").setMessage("This removes local credentials. Disconnect Arafat Assistant in ChatGPT settings if remote access also needs revoking.")
                .setPositiveButton("Remove",(d,w)->state.start(()->{ new SecureStore(this).clear(); state.auth=new AuthSession(this); state.models=new JSONArray(); state.post("Local connection removed. Select Continue with ChatGPT."); }))
                .setNegativeButton("Cancel",null).show();
        });
        button("Source and setup guide",()->open("https://github.com/arafat-247/arafat-portfolio/tree/main/android"));
        state.attach(this);
    }
    private int dp(int n) { return Math.round(n*getResources().getDisplayMetrics().density); }
    private TextView text(String value,int size,boolean bold) {
        TextView t=new TextView(this); t.setText(value); t.setTextSize(size); t.setTextColor(0xff102d25); t.setPadding(0,dp(7),0,dp(5)); if(bold) t.setTypeface(null,Typeface.BOLD); page.addView(t); return t;
    }
    private Button button(String label,Runnable r) { Button b=new Button(this); b.setText(label); b.setAllCaps(false); b.setOnClickListener(v->r.run()); page.addView(b); return b; }
    private Button smallButton(LinearLayout row,String label,Runnable r) { Button b=new Button(this); b.setText(label); b.setAllCaps(false); b.setTextSize(11); b.setOnClickListener(v->r.run()); row.addView(b,new LinearLayout.LayoutParams(0,ViewGroup.LayoutParams.WRAP_CONTENT,1)); return b; }
    private void open(String url) { try { startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse(url))); } catch(Exception e) { state.post("No browser was available to open this link."); } }
    void refresh() {
        if(account==null) return;
        account.setText((state.busy?"Working · ":"Ready · ")+(state.auth==null?"Not connected":state.auth.label()));
        for(Button b:new Button[]{signIn,run,voice,refreshModels,choose,disconnect,reset}) if(b!=null) b.setEnabled(!state.busy);
        String signature=state.models.toString();
        if(!signature.equals(modelSignature)) {
            String previous=models.getSelectedItemPosition()>=0 && models.getSelectedItemPosition()<slugs.size()?slugs.get(models.getSelectedItemPosition()):getPreferences(MODE_PRIVATE).getString("model","");
            slugs.clear(); List<String> names=new ArrayList<>();
            for(int i=0;i<state.models.length();i++) { JSONObject m=state.models.optJSONObject(i); if(m!=null) { slugs.add(m.optString("slug")); names.add(m.optString("display_name",m.optString("slug"))); } }
            models.setAdapter(new ArrayAdapter<>(this,android.R.layout.simple_spinner_dropdown_item,names)); if(slugs.contains(previous)) models.setSelection(slugs.indexOf(previous)); modelSignature=signature;
        }
        models.setEnabled(!state.busy);
        String joined=String.join("\n\n",state.messages); if(!joined.isEmpty()) log.setText(joined); else log.setText("Ready. Connect ChatGPT, then try: বাংলায় উত্তর দাও।");
    }
    private void voice() {
        Intent intent=new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            .putExtra(RecognizerIntent.EXTRA_PROMPT,"Speak in the selected language. Review the transcript before Run.")
            .putExtra(RecognizerIntent.EXTRA_PREFER_OFFLINE,offline.isChecked());
        String lang=switch(languages.getSelectedItemPosition()) { case 0->"en-GB"; case 1->"bn-BD"; case 2->"bn-IN"; default->Locale.getDefault().toLanguageTag(); };
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE,lang);
        try { startActivityForResult(intent,VOICE); } catch(ActivityNotFoundException e) { state.post("No speech recognition service is installed. Use your keyboard’s microphone or type the instruction."); }
    }
    @Override protected void onActivityResult(int request,int result,Intent data) {
        super.onActivityResult(request,result,data);
        if(request==VOICE && result==RESULT_OK && data!=null) {
            ArrayList<String> words=data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
            if(words!=null && !words.isEmpty()) { instruction.setText(words.get(0)); state.post("Transcript added. Review and edit it, then press Run instruction."); }
        }
    }
    private void chooseApps() {
        List<ResolveInfo> raw=getPackageManager().queryIntentActivities(new Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER),0);
        Map<String,String> apps=new TreeMap<>();
        for(ResolveInfo info:raw) if(DeviceService.allowedPackage(info.activityInfo.packageName)) apps.put(info.activityInfo.packageName,info.loadLabel(getPackageManager()).toString());
        List<String> packages=new ArrayList<>(apps.keySet()); packages.sort(Comparator.comparing(apps::get,String.CASE_INSENSITIVE_ORDER));
        String[] labels=new String[packages.size()]; boolean[] checks=new boolean[packages.size()]; Set<String> pending=new HashSet<>(selected);
        for(int i=0;i<labels.length;i++) { labels[i]=apps.get(packages.get(i))+"\n"+packages.get(i); checks[i]=selected.contains(packages.get(i)); }
        new AlertDialog.Builder(this).setTitle("Apps allowed for this task").setMultiChoiceItems(labels,checks,(d,i,checked)->{ if(checked) pending.add(packages.get(i)); else pending.remove(packages.get(i)); })
            .setPositiveButton("Use selected",(d,w)->{ selected.clear(); selected.addAll(pending); selectedLabel.setText(selected.isEmpty()?"No apps selected.":String.join("\n",selected)); share.setChecked(false); }).setNegativeButton("Cancel",null).show();
    }
    private void run() {
        String task=instruction.getText().toString().trim(); int index=models.getSelectedItemPosition();
        if(task.isEmpty()) { instruction.setError("Type or dictate an instruction first"); return; }
        if(task.length()>12000) { instruction.setError("Try a shorter instruction"); return; }
        if(state.auth==null || !state.auth.ready() || index<0 || index>=slugs.size()) { state.post("Connect ChatGPT, refresh models and choose an available model first."); return; }
        String model=slugs.get(index); getPreferences(MODE_PRIVATE).edit().putString("model",model).apply();
        Set<String> allowed=share.isChecked()?Set.copyOf(selected):Set.of(); share.setChecked(false);
        state.task(task,model,allowed,this);
    }
    @Override protected void onSaveInstanceState(Bundle out) { super.onSaveInstanceState(out); out.putString("draft",instruction.getText().toString()); }
    @Override protected void onDestroy() { state.detach(this); super.onDestroy(); }
}
