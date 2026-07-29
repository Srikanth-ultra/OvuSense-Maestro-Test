// Navigate to Settings tab via adb shell input tap (HTTP bridge)
// Maestro's tapOn/swipe doesn't work at Settings tab coordinates on CI emulator,
// but adb shell input tap does. This script calls a local HTTP server that
// executes the adb tap command.
var response = http.get('http://localhost:8089/tap_settings');
