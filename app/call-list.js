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
    if (hospital.number === 1) option.selected = true;
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
        return part.digits.length > 0;
      });
  }

  calls.forEach(function (hospital) {
    var card = document.createElement("article");
    card.className = "call" + (hospital.number === 1 ? " current" : "");
    card.id = "call-" + hospital.number;

    var head = document.createElement("div");
    head.className = "call-head";
    addText(head, "span", "call-number", "#" + hospital.number);
    addText(head, "h2", "call-title", hospital.unit);
    card.appendChild(head);

    if (hospital.number === 1) {
      addText(card, "p", "current-label", "Revisão das chamadas #1–#10");
    }

    var details = document.createElement("p");
    details.className = "details";
    addText(details, "span", "", hospital.city + " - " + hospital.state);
    addText(details, "span", "", "CNES " + hospital.cnes);
    card.appendChild(details);

    var phoneList = document.createElement("div");
    phoneList.className = "phones";
    var phones = phoneParts(hospital.phones).map(function (phone) {
      phone.label = "Número da amostra original";
      return phone;
    });
    (hospital.alternatives || []).forEach(function (alternative) {
      phoneParts(alternative.number).forEach(function (phone) {
        Object.assign(phone, alternative);
        phones.push(phone);
      });
    });
    var seen = new Set();
    phones.forEach(function (phone) {
      var key = phone.digits + ":" + phone.extension;
      if (seen.has(key)) return;
      seen.add(key);
      var item = document.createElement("div");
      item.className = "phone-option";
      addText(item, "p", "phone-label", phone.label);
      var valid = /^\d{2}(?:[2-5]\d{7}|9\d{8})$/.test(phone.digits);
      var link = document.createElement(
        valid && !phone.referenceOnly ? "a" : "div",
      );
      link.className =
        "phone-link" + (valid && !phone.referenceOnly ? "" : " unavailable");
      if (valid && !phone.referenceOnly) {
        link.href = "tel:" + carrierCode + phone.digits;
        link.setAttribute(
          "aria-label",
          "Ligar pela " +
            carrierName +
            " para " +
            phone.display +
            ", " +
            phone.label,
        );
      }
      addText(link, "span", "", phone.display);
      addText(
        link,
        "small",
        "",
        !valid
          ? "Revisar formato"
          : phone.referenceOnly
            ? "Referência"
            : "Ligar",
      );
      item.appendChild(link);
      if (!valid)
        addText(
          item,
          "p",
          "phone-note",
          "Formato inválido ou incompleto na fonte; sem discagem automática.",
        );
      if (phone.extension)
        addText(
          item,
          "p",
          "phone-note",
          "Ramal " + phone.extension + ": digite após a chamada conectar.",
        );
      if (phone.note) addText(item, "p", "phone-note", phone.note);
      if (phone.url) {
        var source = addText(
          item,
          "a",
          "phone-source",
          "Ver fonte · consultada em 22/10/2026",
        );
        source.href = phone.url;
        source.target = "_blank";
        source.rel = "noopener noreferrer";
      }
      phoneList.appendChild(item);
    });
    card.appendChild(phoneList);

    if (hospital.sampleOrder !== hospital.number) {
      card.dataset.originalOrder = hospital.sampleOrder;
    }
    if (hospital.sampleOrder === 1) {
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
    if (hospital.number <= 10 && !hospital.alternatives) {
      addText(
        card,
        "p",
        "phone-note",
        "Nenhum número adicional utilizável localizado nesta revisão.",
      );
    }
    container.appendChild(card);
  });
})();
