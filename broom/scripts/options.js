// import from sendToServer.js

const appendDomain = (domain) => {
  const li = document.createElement("li");
  li.textContent = domain;

  // add remove button
  const remove = document.createElement("button");
  remove.textContent = "Remove";
  remove.addEventListener("click", () => {
    chrome.storage.sync.get("domains", (data) => {
      const domains = data.domains || [];
      const index = domains.indexOf(domain);
      if (index > -1) {
        domains.splice(index, 1);
      }
      chrome.storage.sync.set({ domains });
      li.remove();
    });
  });
  li.appendChild(remove);
  document.getElementById("domains").appendChild(li);
};

chrome.storage.sync.get("domains", (data) => {
  if (data.domains && data.domains.length > 0) {
    for (let domain of data.domains) {
      appendDomain(domain);
    }
  }
});

const add = () => {
  const domain = document.getElementById("domain").value;
  chrome.storage.sync.get("domains", (data) => {
    const domains = data.domains || [];
    domains.push(domain);
    chrome.storage.sync.set({ domains });
    appendDomain(domain);

    // clear input
    document.getElementById("domain").value = "";
  });
};

document.getElementById("add").addEventListener("click", add);
document.getElementById("clear").addEventListener("click", () => {
  chrome.storage.sync.set({ domains: [] });
  document.getElementById("domains").innerHTML = "";
});

document.getElementById("load").addEventListener("click", async () => {
  const src = chrome.runtime.getURL("scripts/sendToServer.js");
  const send2server = await import(src);
  console.log("loading");

  //progress bar
  const progress = document.getElementById("progress");
  const progressBar = document.getElementById("progress-bar");
  const progressText = document.getElementById("status");

  progress.style.display = "block";

  chrome.history.search(
    { text: "", maxResults: 1e5, startTime: 0 },
    async (data) => {
      // get page contents
      const getContents = (url) => {
        // retry on 429 after 5 seconds
        const retry = (url) => {
          return new Promise((resolve) => {
            setTimeout(async () => {
              const content = await getContents(url);
              resolve(content);
            }, 5000);
          });
        };

        return new Promise((resolve) => {
          fetch(url, {
            mode: "cors",
            // try to find cached page
            cache: "force-cache",
          })
            .then((res) => {
              if (res.status === 429) {
                //return retry(url);
                return "";
              }
              return res.text();
            })
            .then((content) => {
              // get title and content
              const parser = new DOMParser();
              const doc = parser.parseFromString(content, "text/html");
              const title = doc.title || "";

              resolve({ title, content, tags: [], ptr: url });
            });
        });
      };

      const domainsToIgnore = [
        "chrome://",
        "chrome-extension://",
        "https://chrome.google.com/webstore",
        "https://google.com",
        "https://www.google.com",
      ];

      // filter out domains and check if pdf or image
      for (let i = 0; i < data.length; i++) {
        const item = data[i];
        let ignore = false;
        for (let domain of domainsToIgnore) {
          if (
            item.url.startsWith(domain) ||
            item.url.endsWith(".pdf") ||
            item.url.endsWith(".png") ||
            item.url.endsWith(".jpg") ||
            item.url.endsWith(".jpeg") ||
            item.url.endsWith(".gif")
          ) {
            ignore = true;
            break;
          }
        }
        if (ignore) {
          data.splice(i, 1);
          i--;
        }
      }

      let contents = [];
      // get contents
      for (let i = 0; i < data.length; i++) {
        const item = data[i];

        // update progress bar
        progressText.textContent = item.url;

        const content = await getContents(item.url);

        progressBar.style.width = `${(i / data.length) * 100}%`;

        contents.push(content);
      }

      // delete all with contents == ""
      for (let i = 0; i < contents.length; i++) {
        if (contents[i].content == "") {
          contents.splice(i, 1);
          i--;
        }
      }

      //close progress bar
      progress.style.display = "none";
      progressText.textContent = "";
      progressBar.style.width = "0%";

      send2server.default(contents, (i, len) => {
        progressText.textContent = `Uploading ${i + 1} of ${len}`;
        progressBar.style.width = `${((i + 1) / len) * 100}%`;
      });
    }
  );
});
