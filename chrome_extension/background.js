//chrome.runtime.onInstalled.addListener(() => {
//  console.log("Extension installed!");
//});
//
//chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
//  if (message === "scanPage") {
//    console.log("Received scanPage request");
//    sendResponse("Page scanned!");
//  }
//  return true; // Important to keep the message channel open
//});
chrome.runtime.onInstalled.addListener(() => {
  console.log("Background service worker installed.");
});
