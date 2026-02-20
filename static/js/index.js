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
    a.textContent = `Download ${file.name}`;
    a.style.display = "block";
    inbox.appendChild(a);
  });
}

async function loadDevices() {
  const r = await fetch("/devices");
  const devices = await r.json();

  const select = document.getElementById("devices");
  select.innerHTML = ""; 

  devices.forEach(device => {
    const option = document.createElement("option");
    option.value = device.index;
    option.textContent = device.name;
    select.appendChild(option);
  });
}

loadDevices();

setInterval(loadInbox, 2000);
setInterval(loadDevices, 2000);

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