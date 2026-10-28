package com.arafat.assistant;
import android.app.Activity;
import android.os.Bundle;
import android.widget.*;
public class FixtureActivity extends Activity {
    @Override public void onCreate(Bundle b) {
        super.onCreate(b); LinearLayout layout=new LinearLayout(this); layout.setOrientation(LinearLayout.VERTICAL);
        TextView title=new TextView(this); title.setText("বাংলা পরীক্ষার পাতা"); layout.addView(title);
        EditText field=new EditText(this); field.setHint("Test input"); field.setContentDescription("Test input"); layout.addView(field);
        EditText password=new EditText(this); password.setInputType(129); password.setText("NEVER_SHARE_PASSWORD"); layout.addView(password);
        Button button=new Button(this); button.setText("Test click"); button.setOnClickListener(v->title.setText("Action clicked")); layout.addView(button);
        setContentView(layout);
    }
}
