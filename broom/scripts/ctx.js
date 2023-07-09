(async function () {
  const src = chrome.runtime.getURL("scripts/sendToServer.js");
  const send2server = await import(src);

  const websiteList = [];
  const website = {
    title: document.title,
    content: document.body.innerText.replaceAll("\n\n", ""),
    ptr: window.location.href,
    tags: [],
  };
  websiteList.push(website);
  send2server.default(websiteList);
})();
