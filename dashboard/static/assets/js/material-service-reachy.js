const makeOneServiceCard = (service) => {
    displayer = document.getElementById("displayerServiceCards");

    const card = document.createElement("div");
    card.className = "card col-sm-4 my-3";

    var cardHeader = document.createElement("h5");
    cardHeader.className = "card-header text-center";
    cardHeader.innerHTML = service;
    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("id", "headerSvg_"+service)
    svg.setAttribute("height",16);
    svg.setAttribute("width",16);
    document.body.appendChild(svg);
    var circles = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circles.setAttribute("cx",10);
    circles.setAttribute("cy",7);
    circles.setAttribute("r",6);
    svg.appendChild(circles);
    cardHeader.appendChild(svg);

    const cardBody = document.createElement("div");
    cardBody.className = "card-body text-center";

    const restartButton = document.createElement("button");
    restartButton.className = "btn bg-pollen-dark-blue btn-md mt-1";
    restartButton.id = service+"_restartButton";
    restartButton.innerHTML = "Restart";
    restartButton.onclick = () => restartService(service);

    const stopButton = document.createElement("button");
    stopButton.className = "btn bg-pollen-dark-blue btn-md mt-1 ms-3";
    restartButton.id = "stopButton";
    stopButton.innerHTML = "Stop";
    stopButton.onclick = () => stopService(service);

    const cardFooter = document.createElement("div");
    cardFooter.className = "card-footer text-center";
    const footerText = document.createElement("i");
    footerText.id = "footerStatus-"+service;
    cardFooter.appendChild(footerText);

    cardBody.appendChild(restartButton);
    cardBody.appendChild(stopButton);

    card.appendChild(cardHeader);
    card.appendChild(cardBody);
    card.appendChild(cardFooter);

    displayer.appendChild(card);
    setFooterStatus(service);
}

makeAllServiceCards = () => {
    const request = new XMLHttpRequest();
    request.onload = e => {
      const serviceList = JSON.parse(request.response);
      for (var i = 0; i < serviceList.length; i++) {
          makeOneServiceCard(serviceList[i]);
      }
    }
    request.open("GET", "/api/list_services");
    request.send();
}

stopService = (service) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/stop_service", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(service));
    setFooterStatus(service);
}

restartService = (service) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/restart_service", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(service));
    setFooterStatus(service);
}

setFooterStatus = (service) => {
    const footer = document.getElementById("footerStatus-"+service);
    const headerSvg = document.getElementById("headerSvg_"+service);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/is_service_running", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = e => {
        const serviceStatus = JSON.parse(xhr.response);
        console.log(serviceStatus);
        footer.innerHTML = serviceStatus;
        if (serviceStatus == 'running') {
            headerSvg.setAttribute("fill", "#c14949");
        }
        else {
            headerSvg.setAttribute("fill", "");
        }

      }
    xhr.send(JSON.stringify(service));
}
