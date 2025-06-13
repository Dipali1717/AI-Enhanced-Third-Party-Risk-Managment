chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "scanPage") {
    const bodyText = document.body.innerText;
    sendResponse({ content: bodyText });
  }
});
