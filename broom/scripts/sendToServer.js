async function sendWebsitesToServer(websiteList, callback = (x, y) => {}) {
  // validate schema
  var valid = true;
  for (var i = 0; i < websiteList.length; i++) {
    var website = websiteList[i];
    if (!website.title || !website.ptr || !website.tags) {
      valid = false;
      break;
    }
  }

  if (!valid) {
    console.log("invalid schema");
    return;
  }

  // send to server
  for (var i = 0; i < websiteList.length; i++) {
    var website = websiteList[i];
    await addDoc(website.title, website.ptr, website.tags, website.content);

    callback(i, websiteList.length);
  }
}

async function addDoc(title, ptr, tags, content) {
  /* var xhr = new XMLHttpRequest();
  xhr.open("POST", "http://localhost:8000/putDoc");
  xhr.setRequestHeader("Content-Type", "application/json");

  xhr.send(JSON.stringify({ title, ptr, tags, content })); */
  await fetch("http://localhost:8000/putDoc", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title, ptr, tags, content }),
  });

  return;
}

export default sendWebsitesToServer;
