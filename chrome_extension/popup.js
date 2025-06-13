//document.getElementById("scanBtn").addEventListener("click", () => {
//  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
//    const tabId = tabs[0].id;
//
//    // Inject content script before messaging
//    chrome.scripting.executeScript({
//      target: { tabId: tabId },
//      files: ["contentScript.js"]
//    }, () => {
//      // Now send message to content script
//      chrome.tabs.sendMessage(tabId, { action: "scanPage" }, (response) => {
//        if (chrome.runtime.lastError) {
//          console.error("Message error:", chrome.runtime.lastError.message);
//          document.getElementById("result").innerText = "Failed to communicate with the tab.";
//          return;
//        }
//
//        if (response) {
//          fetch("http://localhost:5000/analyze_text", {
//            method: "POST",
//            headers: {
//              "Content-Type": "application/x-www-form-urlencoded",
//            },
//            body: new URLSearchParams({
//              text: response.content
//            })
//          })
//            .then(res => res.text())
//            .then(() => {
//              document.getElementById("result").innerText = "Scan complete. Check Flask app.";
//            })
//            .catch(() => {
//              document.getElementById("result").innerText = "Backend request failed.";
//            });
//        }
//      });
//    });
//  });
//});

document.getElementById("scanBtn").addEventListener("click", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const tabId = tabs[0].id;

    // Inject contentScript if not already injected
    chrome.scripting.executeScript({
      target: { tabId: tabId },
      files: ["contentScript.js"]
    }, () => {
      chrome.tabs.sendMessage(tabId, { action: "scanPage" }, (response) => {
        if (chrome.runtime.lastError) {
          console.error("Message error:", chrome.runtime.lastError.message);
          document.getElementById("result").innerText = "Error communicating with tab.";
          return;
        }

        if (response) {
          fetch("http://localhost:5000/analyze_text", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: response.content })
          })
          .then(res => res.json())
          .then(data => {
            document.getElementById("result").innerText = "Scan Result:\n" + data.result;
          })
          .catch(err => {
            console.error("Fetch error:", err);
            document.getElementById("result").innerText = "Failed to reach backend.";
          });
        }
      });
    });
  });
});
