package com.arafat.assistant;

import android.app.*;
import android.content.*;
import android.graphics.Typeface;
import android.net.Uri;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.view.*;
import android.widget.*;
import org.json.*;
import java.util.*;

public final class VoiceActivity extends Activity {
    private VoiceState state;
    private LinearLayout page;
    private EditText instruction;
    private TextView account,log;
    private Spinner models,languages;
    private Button stop;
    private CheckBox offline;
    private final List<Button> idleButtons=new ArrayList<>();
    private final List<String> slugs=new ArrayList<>();
    private String modelSignature="";
    static final int VOICE=42;
    @Override public void onCreate(Bundle saved) {
        super.onCreate(saved); state=VoiceState.get(this);
        ScrollView scroll=new ScrollView(this); scroll.setFillViewport(true); scroll.setBackgroundColor(0xfff3f7f5);
        scroll.setOnApplyWindowInsetsListener((v,insets)->{ v.setPadding(insets.getSystemWindowInsetLeft(),insets.getSystemWindowInsetTop(),insets.getSystemWindowInsetRight(),insets.getSystemWindowInsetBottom()); return insets; });
        page=new LinearLayout(this); page.setOrientation(LinearLayout.VERTICAL); page.setPadding(dp(20),dp(20),dp(20),dp(28)); scroll.addView(page); setContentView(scroll);
        text("ARAFAT VOICE",12,true); text("Ask in your own language.",27,true);
        text("Voice dictation and text · English · বাংলা · other supported languages",14,false);
        text("Voice and text only. This edition cannot read your screen, browse websites or control other apps.",14,true);
        account=text("Preparing local connection…",14,true);
        idle("Continue with ChatGPT",()->state.signIn());
        LinearLayout row=new LinearLayout(this); page.addView(row);
        small(row,"Refresh models",()->state.loadModels());
        small(row,"Manage usage",()->open("https://chatgpt.com/settings/usage"));
        small(row,"Sign out",()->state.start(()->{
            boolean revoked=state.auth!=null && state.auth.signOut(); state.models=new JSONArray(); state.conversation.clear();
            state.main.post(()->{ state.messages.clear(); state.post(revoked?"Signed out.":"Local credentials removed. Remote revocation was not confirmed. Disconnect this app in ChatGPT settings."); });
        }));
        text("Uses an eligible ChatGPT plan and its existing limits. No API key or separately billed API fallback. Account eligibility is checked during sign-in.",13,false);
        text("Model",14,true); models=new Spinner(this); page.addView(models);
        text("Your message / আপনার কথা",17,true);
        instruction=new EditText(this); instruction.setId(R.id.instruction); instruction.setHint("বাংলায় উত্তর দাও। / Type a message…"); instruction.setMinLines(3); instruction.setMaxLines(8); instruction.setGravity(Gravity.TOP);
        instruction.setInputType(android.text.InputType.TYPE_CLASS_TEXT|android.text.InputType.TYPE_TEXT_FLAG_MULTI_LINE|android.text.InputType.TYPE_TEXT_FLAG_CAP_SENTENCES); page.addView(instruction);
        if(saved!=null) instruction.setText(saved.getString("draft",""));
        languages=new Spinner(this); languages.setAdapter(new ArrayAdapter<>(this,android.R.layout.simple_spinner_dropdown_item,new String[]{"English","বাংলা (বাংলাদেশ)","বাংলা (ভারত)","Phone language"})); page.addView(languages);
        offline=new CheckBox(this); offline.setText("Prefer offline dictation, if available"); offline.setChecked(true); page.addView(offline);
        idle("Dictate message",this::voice);
        text("Your phone’s speech service handles dictation and may process audio online. Language support depends on that service. Review the transcript before Send. No background listening.",13,false);
        idle("Send message",this::send);
        stop=button("Stop request",()->state.stop());
        idle("New conversation",()->state.clearConversation());
        text("Replies",18,true); log=text("Ready. Connect ChatGPT, then type or dictate a message.",15,false); log.setId(R.id.reply_log); log.setTextIsSelectable(true);
        text("Recent conversation context stays in memory while this app runs. Up to eight completed exchanges are kept. New conversation clears it. This app does not import your ChatGPT history.",13,false);
        idle("Reset local connection",()->new AlertDialog.Builder(this).setTitle("Remove this phone’s saved connection?")
            .setMessage("This removes local credentials and conversation context. Disconnect the app in ChatGPT settings if remote access also needs revoking.")
            .setPositiveButton("Remove",(d,w)->state.start(()->{ new SecureStore(this).clear(); state.auth=new AuthSession(this); state.models=new JSONArray(); state.conversation.clear(); state.post("Local connection removed. Select Continue with ChatGPT."); }))
            .setNegativeButton("Cancel",null).show());
        button("Source and setup guide",()->open("https://github.com/arafat-247/arafat-portfolio/tree/main/android-voice"));
        state.attach(this);
    }
    private int dp(int n) { return Math.round(n*getResources().getDisplayMetrics().density); }
    private TextView text(String value,int size,boolean bold) { TextView t=new TextView(this); t.setText(value); t.setTextSize(size); t.setTextColor(0xff102d25); t.setPadding(0,dp(7),0,dp(5)); if(bold) t.setTypeface(null,Typeface.BOLD); page.addView(t); return t; }
    private Button button(String label,Runnable action) { Button b=new Button(this); b.setText(label); b.setAllCaps(false); b.setOnClickListener(v->action.run()); page.addView(b); return b; }
    private void idle(String label,Runnable action) { idleButtons.add(button(label,action)); }
    private void small(LinearLayout row,String label,Runnable action) { Button b=new Button(this); b.setText(label); b.setAllCaps(false); b.setTextSize(11); b.setOnClickListener(v->action.run()); row.addView(b,new LinearLayout.LayoutParams(0,ViewGroup.LayoutParams.WRAP_CONTENT,1)); idleButtons.add(b); }
    private void open(String url) { try { startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse(url))); } catch(ActivityNotFoundException e) { state.post("No browser was available to open this link."); } }
    void refresh() {
        if(account==null) return;
        account.setText((state.busy?"Working · ":"Ready · ")+(state.auth==null?"Not connected":state.auth.label()));
        for(Button b:idleButtons) b.setEnabled(!state.busy);
        stop.setEnabled(state.busy);
        String signature=state.models.toString();
        if(!signature.equals(modelSignature)) {
            String previous=models.getSelectedItemPosition()>=0 && models.getSelectedItemPosition()<slugs.size()?slugs.get(models.getSelectedItemPosition()):getPreferences(MODE_PRIVATE).getString("model","");
            slugs.clear(); List<String> names=new ArrayList<>();
            for(int i=0;i<state.models.length();i++) { JSONObject m=state.models.optJSONObject(i); if(m!=null) { slugs.add(m.optString("slug")); names.add(m.optString("display_name",m.optString("slug"))); } }
            models.setAdapter(new ArrayAdapter<>(this,android.R.layout.simple_spinner_dropdown_item,names)); if(slugs.contains(previous)) models.setSelection(slugs.indexOf(previous)); modelSignature=signature;
        }
        models.setEnabled(!state.busy);
        log.setText(state.messages.isEmpty()?"Ready. Connect ChatGPT, then type or dictate a message.":String.join("\n\n",state.messages));
    }
    Intent voiceIntent() {
        String lang=switch(languages.getSelectedItemPosition()) { case 0->"en-GB"; case 1->"bn-BD"; case 2->"bn-IN"; default->Locale.getDefault().toLanguageTag(); };
        return new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            .putExtra(RecognizerIntent.EXTRA_PROMPT,"Speak, then review the transcript before Send.").putExtra(RecognizerIntent.EXTRA_PREFER_OFFLINE,offline.isChecked()).putExtra(RecognizerIntent.EXTRA_LANGUAGE,lang);
    }
    private void voice() { try { startActivityForResult(voiceIntent(),VOICE); } catch(ActivityNotFoundException e) { state.post("No speech recognition service is installed. Use your keyboard’s microphone or type a message."); } }
    @Override protected void onActivityResult(int request,int result,Intent data) {
        super.onActivityResult(request,result,data);
        if(request==VOICE && result==RESULT_OK && data!=null) { ArrayList<String> words=data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS); if(words!=null && !words.isEmpty()) { instruction.setText(words.get(0)); state.post("Transcript added. Review and edit it, then press Send message."); } }
    }
    private void send() {
        String message=instruction.getText().toString().trim(); int index=models.getSelectedItemPosition();
        if(message.isEmpty()) { instruction.setError("Type or dictate a message first"); return; }
        if(message.length()>12000) { instruction.setError("Try a shorter message"); return; }
        if(state.auth==null || !state.auth.ready() || index<0 || index>=slugs.size()) { state.post("Connect ChatGPT, refresh models and choose an available model first."); return; }
        String model=slugs.get(index); getPreferences(MODE_PRIVATE).edit().putString("model",model).apply(); state.task(message,model);
    }
    @Override protected void onSaveInstanceState(Bundle out) { super.onSaveInstanceState(out); out.putString("draft",instruction.getText().toString()); }
    @Override protected void onDestroy() { state.detach(this); super.onDestroy(); }
}
