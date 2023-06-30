// get main non-popul page html

(async () => {
    const src = chrome.runtime.getURL("scripts/sendToServer.js");
    const send2server = await import(src);

    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const tab = tabs[0];
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            files: ['scripts/ctx.js']
        });
    });
})();
