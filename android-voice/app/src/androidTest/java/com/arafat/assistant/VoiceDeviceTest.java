package com.arafat.assistant;

import android.app.*;
import android.content.*;
import android.content.pm.*;
import android.speech.RecognizerIntent;
import android.widget.EditText;
import androidx.test.platform.app.InstrumentationRegistry;
import androidx.test.rule.ActivityTestRule;
import androidx.test.uiautomator.*;
import org.json.JSONObject;
import org.junit.*;
import static org.junit.Assert.*;
import java.util.*;

public class VoiceDeviceTest {
    @Rule public ActivityTestRule<VoiceActivity> activity=new ActivityTestRule<>(VoiceActivity.class);
    @Test public void installedPackageHasNoSensitiveServicesOrPermissions() throws Exception {
        Context c=InstrumentationRegistry.getInstrumentation().getTargetContext();
        assertEquals("com.arafat.assistant.voice",c.getPackageName());
        PackageInfo info=c.getPackageManager().getPackageInfo(c.getPackageName(),PackageManager.GET_SERVICES|PackageManager.GET_RECEIVERS|PackageManager.GET_PROVIDERS|PackageManager.GET_PERMISSIONS);
        assertTrue(info.services==null || info.services.length==0); assertTrue(info.receivers==null || info.receivers.length==0); assertTrue(info.providers==null || info.providers.length==0);
        assertArrayEquals(new String[]{"android.permission.INTERNET"},info.requestedPermissions);
        SecureStore store=new SecureStore(c); store.save(new JSONObject().put("test_secret","local-only-value"));
        assertEquals("local-only-value",store.load().getString("test_secret"));
        assertFalse(c.getSharedPreferences("protected-chatgpt",0).getString("record","").contains("local-only-value")); store.clear();
        UiDevice device=UiDevice.getInstance(InstrumentationRegistry.getInstrumentation());
        assertTrue(device.wait(Until.hasObject(By.text("Continue with ChatGPT")),10000));
        assertFalse(device.hasObject(By.text("Open Android Accessibility settings")));
        device.executeShellCommand("screencap -p /sdcard/Download/arafat-voice-main.png");
    }
    @Test public void banglaTranscriptRequiresReviewAndSurvivesRecreation() throws Exception {
        Instrumentation i=InstrumentationRegistry.getInstrumentation();
        String text="বাংলায় উত্তর দাও।";
        i.runOnMainSync(()->{
            VoiceActivity a=activity.getActivity();
            assertEquals(RecognizerIntent.ACTION_RECOGNIZE_SPEECH,a.voiceIntent().getAction());
            assertTrue(a.voiceIntent().getBooleanExtra(RecognizerIntent.EXTRA_PREFER_OFFLINE,false));
            a.onActivityResult(VoiceActivity.VOICE,Activity.RESULT_OK,new Intent().putStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS,new ArrayList<>(List.of(text))));
        });
        i.waitForIdleSync();
        i.runOnMainSync(()->assertEquals(text,((EditText)activity.getActivity().findViewById(R.id.instruction)).getText().toString()));
        assertFalse(VoiceState.get(i.getTargetContext()).busy);
        i.runOnMainSync(()->activity.getActivity().recreate());
        UiDevice device=UiDevice.getInstance(i);
        assertTrue(device.wait(Until.hasObject(By.res(i.getTargetContext().getPackageName(),"instruction").text(text)),10000));
    }
}
