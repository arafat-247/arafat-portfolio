package com.arafat.assistant;

import org.json.*;
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;

final class Http {
    private Http() {}
    static HttpURLConnection open(String url,String token,String body,String type) throws Exception {
        URL parsed=new URL(url);
        if(!parsed.getProtocol().equals("https") || !(parsed.getHost().equals("auth.openai.com") || parsed.getHost().equals("api.openai.com"))) throw new IOException("Untrusted connection address");
        HttpURLConnection c=(HttpURLConnection)parsed.openConnection();
        c.setInstanceFollowRedirects(false); c.setConnectTimeout(15000); c.setReadTimeout(45000);
        c.setRequestProperty("Accept", "application/json".equals(type)?"text/event-stream":"application/json");
        if(token!=null) c.setRequestProperty("Authorization","Bearer "+token);
        if(body!=null) {
            c.setRequestMethod("POST"); c.setDoOutput(true); c.setRequestProperty("Content-Type",type);
            try(OutputStream out=c.getOutputStream()) { out.write(body.getBytes(StandardCharsets.UTF_8)); }
        }
        return c;
    }
    static String read(InputStream in,int max) throws IOException {
        if(in==null) return "";
        try(in; ByteArrayOutputStream out=new ByteArrayOutputStream()) {
            byte[] b=new byte[4096]; int n;
            while((n=in.read(b))!=-1) { if(out.size()+n>max) throw new IOException("Server response too large"); out.write(b,0,n); }
            return out.toString("UTF-8");
        }
    }
    static void ok(HttpURLConnection c) throws Exception {
        int status=c.getResponseCode(); if(status>=200 && status<300) return;
        String code="";
        try { JSONObject e=new JSONObject(read(c.getErrorStream(),16000)).optJSONObject("error"); if(e!=null) code=e.optString("code"); } catch(Exception ignored) {}
        throw new IOException(Protocol.error(code,status));
    }
    static JSONObject json(String url,String token,String body) throws Exception {
        HttpURLConnection c=open(url,token,body,"application/x-www-form-urlencoded");
        try { ok(c); return new JSONObject(read(c.getInputStream(),2_000_000)); } finally { c.disconnect(); }
    }
}
