package com.arafat.assistant;

import android.content.*;
import android.os.SystemClock;
import android.app.Instrumentation;
import androidx.test.platform.app.InstrumentationRegistry;
import androidx.test.uiautomator.*;
import org.json.*;
import org.junit.*;
import static org.junit.Assert.*;
import java.util.Set;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicBoolean;

public class DeviceTest {
    static {
        // UiAutomator otherwise suppresses the service we are trying to test.
        Configurator.getInstance().setUiAutomationFlags(android.app.UiAutomation.FLAG_DONT_SUPPRESS_ACCESSIBILITY_SERVICES);
    }
    private final Instrumentation instrumentation=InstrumentationRegistry.getInstrumentation();
    private final UiDevice device=UiDevice.getInstance(instrumentation);
    @Test public void packagedUiAndEncryptedStorage() throws Exception {
        Context c=instrumentation.getTargetContext();
        SecureStore store=new SecureStore(c); JSONObject record=new JSONObject().put("test_secret","not-plaintext");
        store.save(record); assertEquals("not-plaintext",store.load().getString("test_secret"));
        assertFalse(c.getSharedPreferences("protected-chatgpt",0).getString("record","").contains("not-plaintext")); store.clear();
        c.startActivity(new Intent(c,MainActivity.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
        assertTrue(device.wait(Until.hasObject(By.text("Continue with ChatGPT")),10000));
        assertTrue(device.hasObject(By.text("Run instruction")) || device.findObject(new UiSelector().scrollable(true)).exists());
        device.executeShellCommand("screencap -p /sdcard/Download/arafat-main.png");
    }
    @Test public void selectedScreenApprovalAndStopAreEnforced() throws Exception {
        Context app=instrumentation.getTargetContext(),test=instrumentation.getContext();
        device.executeShellCommand("settings put secure enabled_accessibility_services com.arafat.assistant/.DeviceService");
        device.executeShellCommand("settings put secure accessibility_enabled 1");
        long deadline=SystemClock.elapsedRealtime()+15000;
        while(DeviceService.instance==null && SystemClock.elapsedRealtime()<deadline) Thread.sleep(100);
        DeviceService service=DeviceService.instance; assertNotNull(service);
        AtomicBoolean cancelled=new AtomicBoolean();
        ExecutorService worker=Executors.newSingleThreadExecutor();
        try {
            test.startActivity(new Intent().setComponent(new ComponentName(test.getPackageName(),FixtureActivity.class.getName())).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
            boolean visible=device.wait(Until.hasObject(By.text("Test click")),10000);
            device.executeShellCommand("screencap -p /sdcard/Download/arafat-fixture.png");
            if(!visible) {
                java.io.ByteArrayOutputStream dump=new java.io.ByteArrayOutputStream(); device.dumpWindowHierarchy(dump);
                String xml=dump.toString("UTF-8"); for(int k=0;k<xml.length();k+=3500) android.util.Log.i("ArafatTestHierarchy",xml.substring(k,Math.min(k+3500,xml.length())));
            }
            assertTrue("Fixture app did not open",visible);
            service.begin(Set.of(test.getPackageName()),cancelled,()->cancelled.set(true));
            Thread.sleep(500);
            JSONObject shot=new JSONObject(service.snapshot()); assertEquals(test.getPackageName(),shot.getString("package"));
            assertTrue(shot.toString().contains("বাংলা পরীক্ষার পাতা")); assertFalse(shot.toString().contains("NEVER_SHARE_PASSWORD"));
            JSONArray nodes=shot.getJSONArray("nodes"); String id="";
            for(int i=0;i<nodes.length();i++) if(nodes.getJSONObject(i).optString("text").equals("Test click")) id=nodes.getJSONObject(i).getString("id");
            assertFalse(id.isEmpty()); final String target=id;
            Future<String> result=worker.submit(()->service.execute("click",new JSONObject().put("id",target)));
            UiObject2 approve=device.wait(Until.findObject(By.text("Approve").enabled(true)),8000); assertNotNull(approve);
            assertFalse(result.isDone()); assertFalse(shot.toString().contains("Action clicked"));
            device.executeShellCommand("screencap -p /sdcard/Download/arafat-approval.png");
            approve.click(); assertTrue(result.get(10,TimeUnit.SECONDS).startsWith("Action completed"));
            // The overlay is the active accessibility window after approval. The service
            // must still identify the focused application underneath it.
            assertThrows(Exception.class,()->service.execute("click",new JSONObject().put("id",target)));
            JSONObject changed=new JSONObject(service.snapshot());
            assertTrue(changed.toString().contains("Action clicked"));
            JSONArray fresh=changed.getJSONArray("nodes"); String field="";
            for(int i=0;i<fresh.length();i++) if(fresh.getJSONObject(i).optBoolean("editable")) { field=fresh.getJSONObject(i).getString("id"); break; }
            assertFalse(field.isEmpty()); final String editable=field;
            String replacement="বাংলা লেখার পরীক্ষা সফল হয়েছে। ".repeat(12);
            Future<String> typed=worker.submit(()->service.execute("type_text",new JSONObject().put("id",editable).put("text",replacement)));
            UiObject2 allowText=device.wait(Until.findObject(By.text("Approve").enabled(true)),8000); assertNotNull(allowText); assertFalse(typed.isDone());
            device.executeShellCommand("screencap -p /sdcard/Download/arafat-text-review.png");
            allowText.click(); assertTrue(typed.get(10,TimeUnit.SECONDS).startsWith("Action completed"));
            assertTrue(service.snapshot().contains("বাংলা লেখার পরীক্ষা"));
            app.startActivity(new Intent(app,MainActivity.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
            Thread.sleep(800); assertThrows(Exception.class,service::snapshot);
            device.findObject(By.text("Stop")).click(); Thread.sleep(300);
            assertTrue(cancelled.get()); assertThrows(Exception.class,service::snapshot);
        } finally {
            service.finish(); instrumentation.waitForIdleSync(); worker.shutdownNow();
            device.executeShellCommand("settings delete secure enabled_accessibility_services");
            device.executeShellCommand("settings put secure accessibility_enabled 0");
        }
    }
}
