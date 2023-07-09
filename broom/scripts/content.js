chrome.storage.sync.get("domains", async (data) => {
  const src = chrome.runtime.getURL("scripts/sendToServer.js");
  const send2server = await import(src);

  //check if current domain is in domains
  if (data.domains && data.domains.length > 0) {
    for (let domain of data.domains) {
      if (
        window.location.href.includes(domain) &&
        !(
          window.location.href.endsWith(".pdf") ||
          window.location.href.endsWith(".png") ||
          window.location.href.endsWith(".jpg") ||
          window.location.href.endsWith(".jpeg") ||
          window.location.href.endsWith(".gif")
        )
      ) {
        //send to server
        const websiteList = [];
        const website = {
          title: document.title,
          content: document.body.innerText,
          ptr: window.location.href,
          tags: [],
        };
        websiteList.push(website);
        send2server.default(websiteList, (i, len) => {
          console.log("done!");
        });
        break;
      }
    }
  }
});
