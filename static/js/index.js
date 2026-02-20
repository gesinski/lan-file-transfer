const container = document.getElementById("container");
const CURRENT_DEVICE = parseInt(container.dataset.deviceIndex, 10);

async function loadInbox() {
  const r = await fetch("/inbox");
  const files = await r.json();

  const inbox = document.getElementById("inbox");
  inbox.innerHTML = "";

  files.forEach(file => {
    const a = document.createElement("a");
    a.href = `/download/${CURRENT_DEVICE}/${file.name}`;
    a.textContent = `Download ${file.name} (from device ${file.sender})`;
    a.style.display = "block";
    inbox.appendChild(a);
  });
}

setInterval(loadInbox, 2000);

document.getElementById("uploadForm").onsubmit = async e => {
  e.preventDefault();

  const formData = new FormData(e.target);
  const select = document.getElementById("devices");
  formData.set("devices", select.value);

  await fetch("/upload", {
    method: "POST",
    body: formData
  });

  loadInbox();
};