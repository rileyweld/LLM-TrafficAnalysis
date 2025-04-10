chrome.tabs.onActivated.addListener(async (activeInfo) => {
    const tab = await chrome.tabs.get(activeInfo.tabId);
    sendUrl(tab.url);
});
  
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === "complete" && tab.active) {
      sendUrl(tab.url);
    }
});
  
function sendUrl(url) {
    console.log("Trying to send URL:", url); 
    fetch("http://localhost:5050/receive-url", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url })
    }).then(() => console.log("Sent URL:", url));
}
