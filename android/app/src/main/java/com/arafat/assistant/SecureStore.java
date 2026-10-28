package com.arafat.assistant;

import android.content.Context;
import android.content.SharedPreferences;
import android.security.keystore.*;
import org.json.JSONObject;
import javax.crypto.*;
import javax.crypto.spec.GCMParameterSpec;
import java.security.KeyStore;
import java.util.Base64;

/** Credentials are AES-GCM encrypted with a non-exportable Android Keystore key. */
final class SecureStore {
    private final SharedPreferences prefs;
    SecureStore(Context c) { prefs=c.getSharedPreferences("protected-chatgpt",Context.MODE_PRIVATE); }
    private SecretKey key() throws Exception {
        KeyStore store=KeyStore.getInstance("AndroidKeyStore"); store.load(null);
        String alias="arafat-chatgpt-v1";
        if(!store.containsAlias(alias)) {
            KeyGenerator gen=KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES,"AndroidKeyStore");
            gen.init(new KeyGenParameterSpec.Builder(alias,KeyProperties.PURPOSE_ENCRYPT|KeyProperties.PURPOSE_DECRYPT)
                .setBlockModes(KeyProperties.BLOCK_MODE_GCM).setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE).build()); gen.generateKey();
        }
        return (SecretKey)store.getKey(alias,null);
    }
    synchronized JSONObject load() throws Exception {
        String value=prefs.getString("record",null); if(value==null) return new JSONObject();
        String[] parts=value.split(":");
        Cipher c=Cipher.getInstance("AES/GCM/NoPadding"); c.init(Cipher.DECRYPT_MODE,key(),new GCMParameterSpec(128,Base64.getDecoder().decode(parts[0])));
        return new JSONObject(new String(c.doFinal(Base64.getDecoder().decode(parts[1])),java.nio.charset.StandardCharsets.UTF_8));
    }
    synchronized void save(JSONObject record) throws Exception {
        Cipher c=Cipher.getInstance("AES/GCM/NoPadding"); c.init(Cipher.ENCRYPT_MODE,key());
        String value=Base64.getEncoder().encodeToString(c.getIV())+":"+Base64.getEncoder().encodeToString(c.doFinal(record.toString().getBytes(java.nio.charset.StandardCharsets.UTF_8)));
        if(!prefs.edit().putString("record",value).commit()) throw new java.io.IOException("Could not save the ChatGPT connection");
    }
    synchronized void clear() { prefs.edit().remove("record").commit(); }
}
