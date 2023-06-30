chrome.storage.sync.get("domains", async (data) => {
  const src = chrome.runtime.getURL("scripts/sendToServer.js");
  const send2server = await import(src);

  //check if current domain is in domains
  if (data.domains && data.domains.length > 0) {
    for (let domain of data.domains) {
      if (window.location.hostname.includes(domain)) {
        //send to server
        const websiteList = [];
        const website = {
          title: document.title,
          content: document.body.innerText,
          tags: [],
        };
        websiteList.push(website);
        send2server.default(websiteList);
        break;
      }
    }
  }
});