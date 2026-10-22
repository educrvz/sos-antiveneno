(function () {
  "use strict";

  var calls = window.SOROJA_CALLS || [];
  var carrier = document.body.dataset.carrier;
  var carrierCode = carrier === "vivo" ? "015" : "021";
  var carrierName = carrier === "vivo" ? "Vivo" : "Claro";
  var container = document.getElementById("calls");
  var jumpNumber = document.getElementById("jump-number");
  var jumpForm = document.getElementById("jump-form");

  calls.forEach(function (hospital) {
    var option = document.createElement("option");
    option.value = hospital.number;
    option.textContent = "Chamada #" + hospital.number + " — " + hospital.unit;
    if (hospital.number === 5) option.selected = true;
    jumpNumber.appendChild(option);
  });

  jumpForm.addEventListener("submit", function (event) {
    event.preventDefault();
    var target = document.getElementById("call-" + jumpNumber.value);
    if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  function addText(parent, tag, className, value) {
    var element = document.createElement(tag);
    if (className) element.className = className;
    element.textContent = value;
    parent.appendChild(element);
    return element;
  }

  function phoneParts(raw) {
    return String(raw || "")
      .split("/")
      .map(function (part) {
        var extensionMatch = part.match(/\bR\.?\s*(\d+)\s*$/i);
        var base = part.replace(/\bR\.?\s*\d+\s*$/i, "");
        return {
          display: part.trim(),
          digits: base.replace(/\D/g, ""),
          extension: extensionMatch ? extensionMatch[1] : "",
        };
      })
      .filter(function (part) {
        return part.digits.length >= 10;
      });
  }

  calls.forEach(function (hospital) {
    var card = document.createElement("article");
    card.className = "call" + (hospital.number === 5 ? " current" : "");
    card.id = "call-" + hospital.number;

    var head = document.createElement("div");
    head.className = "call-head";
    addText(head, "span", "call-number", "#" + hospital.number);
    addText(head, "h2", "call-title", hospital.unit);
    card.appendChild(head);

    if (hospital.number === 5) {
      addText(card, "p", "current-label", "Próxima chamada");
    }

    var details = document.createElement("p");
    details.className = "details";
    addText(details, "span", "", hospital.city + " - " + hospital.state);
    addText(details, "span", "", "CNES " + hospital.cnes);
    card.appendChild(details);

    var phoneList = document.createElement("div");
    phoneList.className = "phones";
    phoneParts(hospital.phones).forEach(function (phone) {
      var link = document.createElement("a");
      link.className = "phone-link";
      link.href = "tel:" + carrierCode + phone.digits;
      link.setAttribute(
        "aria-label",
        "Ligar pela " +
          carrierName +
          " para " +
          hospital.unit +
          ", " +
          phone.display,
      );
      addText(link, "span", "", phone.display);
      addText(link, "small", "", "Ligar");
      phoneList.appendChild(link);
      if (phone.extension) {
        addText(
          card,
          "p",
          "bad-number",
          "Ramal " + phone.extension + ": digite após a chamada conectar.",
        );
      }
    });
    card.appendChild(phoneList);

    if (hospital.sampleOrder !== hospital.number) {
      card.dataset.originalOrder = hospital.sampleOrder;
    }
    if (hospital.sampleOrder === 5) {
      card.dataset.currentCall = "true";
    }
    if (hospital.phones === "(88) 3583-22726") {
      addText(
        card,
        "p",
        "bad-number",
        "Amostra sinaliza formato possivelmente incorreto no número fixo; registre exatamente o que ocorreu.",
      );
    }
    container.appendChild(card);
  });
})();
