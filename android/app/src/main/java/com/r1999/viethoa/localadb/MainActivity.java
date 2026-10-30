package com.r1999.viethoa.localadb;

import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

/**
 * Giao diện chính của Trình Cài Đặt Việt Hóa Reverse: 1999 Android (Local ADB / SAF).
 */
public class MainActivity extends AppCompatActivity {

    public static final String GAME_PACKAGE = "com.bluepoch.m.en.reverse1999";
    private TextView statusTextView;
    private Button patchButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Khởi tạo UI đơn giản dạng code
        android.widget.LinearLayout layout = new android.widget.LinearLayout(this);
        layout.setOrientation(android.widget.LinearLayout.VERTICAL);
        layout.setPadding(40, 40, 40, 40);

        TextView titleView = new TextView(this);
        titleView.setText("REVERSE: 1999 — VIỆT HÓA LIGHT NOVEL");
        titleView.setTextSize(20);
        titleView.setTypeface(null, android.graphics.Typeface.BOLD);
        titleView.setPadding(0, 0, 0, 30);
        layout.addView(titleView);

        statusTextView = new TextView(this);
        statusTextView.setText("Gói game đích: " + GAME_PACKAGE + "\nTrạng thái: Sẵn sàng kết nối Local ADB / Shizuku.");
        statusTextView.setPadding(0, 0, 0, 40);
        layout.addView(statusTextView);

        patchButton = new Button(this);
        patchButton.setText("Cài Đặt / Cập Nhật Việt Hóa 1-Click");
        patchButton.setOnClickListener(v -> {
            Toast.makeText(this, "Bắt đầu tiến trình nạp bản Việt Hóa qua Local ADB...", Toast.LENGTH_SHORT).show();
            statusTextView.setText("Đang đồng bộ gói dịch vào Android/data/" + GAME_PACKAGE + "...");
        });
        layout.addView(patchButton);

        setContentView(layout);
    }
}
