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

    if (!url || url === '') {
      console.log("Skipping empty URL:", url);
      return;
    }

    fetch("http://localhost:5050/receive-url", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Sent URL:", url);
        if (data.verdict === "malicious") {
            chrome.notifications.create({
                type: 'basic',
                iconUrl: 'icon.png',
                title: '⚠️ Malicious Website Detected!',
                message: `Confidence: ${data.confidence}%\nThis site may be dangerous.`,
                priority: 2
            });
        }
    })
    .catch(error => console.error('Error:', error));
}
