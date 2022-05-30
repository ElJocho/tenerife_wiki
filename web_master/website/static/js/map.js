//initializing map on global level, now all functions can directly reference it without passing it as parameter
var southWest = L.latLng(27.9, -17.1);
var northEast = L.latLng(28.7, -15.9);
var bounds = L.latLngBounds(southWest, northEast);
var multiPoint = null;
var multiPointVeggie = null;
var routes_multiLine = null;

// bools used for timeslider sync
let location_isOn = true;
let route_isOn = true;
let vegetation_isOn = false;

// often used elements for js manipulation:

let entry_div = null;
const entry_elements_div = document.getElementById(
  "entry_elements_placeholder"
);
const entry_div_location_title = document.getElementById(
  "placeholder_location_title"
);
const entry_div_image_container = document.getElementById(
  "placeholder_image_container"
);
const entry_div_text = document.getElementById("placeholder_text");
const entry_overlay = document.getElementById("entry_overlay");

document.getElementById("map").innerHTML = "<div id='map' class='map'></div>";
var map = L.map("map", {
  center: [28.2, -16.5],
  zoom: 10,
  minZoom: 10,
  maxBounds: bounds,
});

function getColor(props) {
  switch (props) {
    case "Stone":
      return "#838383";
    case "Stop":
      return "#000";
    case "Hydro":
      return "#00008b";
    case "Soil":
      return "#663300";
    case "Agro":
    case "Plant":
      return "#005c1a";
    case "Data":
      return "#8fa3ad";
    case "Trash":
      return "#ff0000";
  }
}

function getVegetationColor(props) {
  switch (props) {
    case "kanarenkiefernwaelder":
      return "#04916e";
    case "loorbeerwald":
      return "#45b56a";
    case "thermophilebuschwaelder":
      return "#18b9c4";
    case "ziernutzpflanzen":
      return "#ad0a67";
    case "sukkulentenbusch":
      return "#ffd70d";
    case "kuestenvegetation":
      return "#d16b04";
  }
}

async function get_objects(object_string) {
  const data = await fetch(`/api/get_${object_string}`);
  let json = await data.json();
  return json;
}

async function get_entries(l_id) {
  const data = await fetch(`/api/get_entries?l_id=${l_id}`);
  let json = await data.json();
  return json;
}

async function update_entry_div(feature, mode) {
  if ((entry_div == null && mode != "veggie") || mode == "location") {
    entry_div = document.getElementById("placeholder_div");
    entry_div.style.display = "flex";
  } else {
    entry_div = document.getElementById("placeholder_div");
    entry_div.style.display = "none";
  }

  // todo: address the mode spaghetti

  entry_div_location_title.innerHTML = feature.caption
    ? feature.caption
    : feature.name;
  entry_div_image_container.innerHTML =
    '<img src="data:image/' +
    feature.image_data_type +
    ";base64," +
    feature.image +
    '" class="card_img">';
  entry_div_text.innerHTML = feature.text;

  if (mode == "location") {
    let entries = await get_entries(feature.id);

    if (entries.length == 0) {
      entry_elements_div.style.display = "none";
    } else {
      entry_elements_div.style.display = "flex";
    }
    entry_elements_div.innerHTML = "";
    let new_inner = "<ul id='entries' class='card_flex_list'>";
    for (let entry of entries) {
      new_inner += `<li class="card_item" id="entry_${entry.id}">`;
      new_inner += '   <div class="img_container">';
      new_inner += `     <img src="data:image/${entry.image_data_type};base64,${entry.image}" class="card_img"></img>`;
      new_inner += "   </div>";
      new_inner += `   <h2>${entry.title}</h2>`;
      new_inner += `   <p>${entry.category}</p>`;
      new_inner += "</li>";
    }
    new_inner += "</ul>";
    entry_elements_div.innerHTML = new_inner;

    for (let entry of entries) {
      let prof_image = "";
      if (entry.user_image != null) {
        prof_image = `<img src="data:image/${
          entry.user_image_data_type
        };base64,${entry.user_image.slice(
          2,
          -1
        )}"  onclick='window.open("/profile?u_id=${
          entry.user_id
        }", "_self")' class="profile_link">`;
      } else {
        prof_image = `<img src="./static/icons/profile.png" class="profile_link" onclick='window.open("/profile?u_id=${entry.user_id}", "_self")'>`;
      }

      document
        .getElementById(`entry_${entry.id}`)
        .addEventListener("click", (e) => {
          entry_overlay.innerHTML =
            "<div class='inner_overlay flex-column' style='justify-content: flex-start;'>" +
            prof_image +
            "<h1 style='margin-top: 15px;'>" +
            entry.title +
            "</h1>" +
            "<div class='flex-column' style='width: 90%;'>" +
            "<img src='data:image/" +
            entry.image_data_type +
            ";base64," +
            entry.image +
            "' class='preview_img'><p>" +
            entry.text +
            "</p>" +
            "</div></div>";
          $("#entry_overlay").show();
          $("#entry_overlay").addClass("fade_in");
        });
    }
  }
}

async function all_locations() {
  let locations = await get_objects("locations");
  let routes = await get_objects("routes");
  let vegetation = await get_objects("vegetation");

  //Setting for showing all locations on the map
  var geojson = [];
  for (const location of locations) {
    let category =
      location.category != null ? location.category.split("-")[1] : null;
    let point = JSON.parse(location.geojson);
    point["category"] = category;
    point["id"] = location.id;
    point["caption"] = location.caption;
    point["text"] = location.text;
    point["image_data_type"] = location.image_data_type;
    point["image"] = location.image;
    point["name"] = location.name;
    point["day"] = location.name.split("_")[1];
    geojson.push(point);
  }

  var veggieGeojson = [];
  for (const veggie of vegetation) {
    let point = JSON.parse(veggie.geojson);

    point["category"] = veggie.zone;
    point["id"] = veggie.id;
    point["image_bark"] = veggie.image_bark;
    point["image_fruit"] = veggie.image_fruit;
    point["image_habit"] = veggie.image_habit;
    point["image_leaf"] = veggie.image_leaf;
    point["image_flower"] = veggie.image_flower;
    point["current_name"] = veggie.current_name;
    point["author"] = veggie.author;
    point["url"] = veggie.url;
    point["family"] = veggie.family;
    point["day"] = parseInt(veggie.date.split(" ")[1]) - 6;
    veggieGeojson.push(point);
  }

  var routes_geojson = [];

  for (const route of routes) {
    line = JSON.parse(route.geojson);
    line["name"] = route.name.split(" ")[1];

    routes_geojson.push(line);
  }

  var info = L.control();
  info.onAdd = function (map) {
    this._div = L.DomUtil.create("div", "info");
    this.update();
    return this._div;
  };

  info.update = function (props) {
    if (props) {
      let image = props.image_habit
        ? props.image_habit
        : props.image_flower
        ? props.image_flower
        : props.image_leaf;

      this._div.innerHTML =
        '<div class="flex-row"><h4>' +
        (props.caption
          ? props.caption
          : props.name
          ? props.name
          : ` <a target="_blank" href="${props.url}">${props.current_name}</a> `) +
        "</h4>" +
        ' <button class="hero-button small-button" id="project_close" type="button" style="margin-left: auto;">x</button></div>';
      this._div.innerHTML += props.image_data_type
        ? '<img src="data:image/' +
          props.image_data_type +
          ";base64," +
          props.image +
          '" class="card_img card_img_small">'
        : `<img src="${image}" class="card_img card_img_small">`;

      $("#project_close").on("click", (e) => {
        multiPointVeggie.eachLayer((layer) => {
          try {
            multiPointVeggie.resetStyle(layer);
          } catch (e) {}
          layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
            click: highlightFeature,
          });
        });

        multiPoint.eachLayer((layer) => {
          try {
            multiPoint.resetStyle(layer);
          } catch (e) {}
          layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
            click: highlightFeature,
          });
        });
        info.update();
      });
      $("#to_project").on("click", (e) => {
        e.preventDefault();
        go_to = "/project";
        window.open(go_to + window.location.search, "_self");
      });
    } else {
      this._div.innerHTML =
        "<h4>Auf Projekt klicken um Informationen zu bekommen</h4>";
    }
  };

  async function highlightFeature(e) {
    var type = e.type;
    var Layer = e.target;
    Layer.setStyle({
      weight: 5,
      color: "#034e7b",
      opacity: 1,
      dashArray: "3",
      fillOpacity: 0.9,
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
      Layer.bringToFront();
    }
    info.update(Layer.feature.geometry);
    if (type == "click") {
      multiPoint.eachLayer(function (layer) {
        layer.off("mouseout", resetHighlight);
        layer.off("mouseover", highlightFeature);
        if (layer != Layer) {
          try {
            multiPoint.resetStyle(layer);
          } catch (e) {}
        }
      });

      multiPointVeggie.eachLayer(function (layer) {
        layer.off("mouseout", resetHighlight);
        layer.off("mouseover", highlightFeature);
        if (layer != Layer) {
          try {
            multiPointVeggie.resetStyle(layer);
          } catch (e) {}
        }
      });

      update_url("l_id", Layer.feature.geometry.id);

      update_entry_div(
        Layer.feature.geometry,
        Layer.feature.geometry.image_data_type !== undefined
          ? "location"
          : "veggie"
      );
    }
  }

  function resetHighlight(e) {
    info.update();

    multiPointVeggie.eachLayer((layer) => {
      try {
        multiPointVeggie.resetStyle(layer);
      } catch (e) {}
      layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: highlightFeature,
      });
    });

    multiPoint.eachLayer((layer) => {
      try {
        multiPoint.resetStyle(layer);
      } catch (e) {}
      layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: highlightFeature,
      });
    });

    multiPoint.bringToFront();
    multiPointVeggie.bringToFront();
  }

  function onEachFeature(feature, layer) {
    layer.on({
      mouseover: highlightFeature,
      mouseout: resetHighlight,
      click: highlightFeature,
    });
  }

  function geojsonMarkerOptions(target) {
    return {
      radius: 8,
      color: getColor(target.geometry.category),
      weight: 1,
      opacity: 1,
      fillOpacity: 0.7,
    };
  }

  function geojsonVeggieMarkerOptions(target) {
    return {
      radius: 8,
      color: getVegetationColor(target.geometry.category),
      weight: 1,
      opacity: 1,
      fillOpacity: 0.7,
    };
  }

  function styleLines() {
    return {
      color: "blue",
      weight: 3,
      opacity: 0.5,
      lineJoin: "round",
    };
  }
  info.addTo(map);

  multiPoint = L.geoJSON(geojson, {
    pointToLayer: function (feature, latlng) {
      return L.circleMarker(latlng);
    },
    style: geojsonMarkerOptions,
    onEachFeature: onEachFeature,
  }).addTo(map);

  multiPointVeggie = L.geoJSON(veggieGeojson, {
    pointToLayer: function (feature, latlng) {
      return L.circleMarker(latlng);
    },
    style: geojsonVeggieMarkerOptions,
    onEachFeature: onEachFeature,
  });

  routes_multiLine = L.geoJSON(routes_geojson, { style: styleLines }).addTo(
    map
  );
  multiPoint.bringToFront();
  multiPointVeggie.bringToFront();
}

async function initMap() {
  //loading base elements of map and all other needed elements

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    bounds: bounds,
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  // add scale bar
  var scale = L.control.scale({
    imperial: false,
    updateWhenIdle: true,
  });
  scale.addTo(map);

  var legend = L.control({ position: "bottomright" });

  legend.onAdd = () => {
    var div = L.DomUtil.create("div", "info legend");

    let nice_name = {
      Stone: "Geologie",
      Stop: "Autostop",
      Hydro: "Hydrologie",
      Soil: "Bodengeographie",
      Plant: "Biologie und Agrikultur",
      Data: "Datenpunkte",
      Trash: "Recyclinghof",
    };
    let labels = Object.keys(nice_name);

    let nice_veggie_name = {
      kanarenkiefernwaelder: "Kanarenkiefernwald",
      loorbeerwald: "Loorbeerwald",
      thermophilebuschwaelder: "Thermophiler Buschwald",
      ziernutzpflanzen: "Zier- oder Nutzpflanze",
      sukkulentenbusch: "Sukkulentenbusch",
      kuestenvegetation: "Küstenvegetation",
    };
    let veggieLabels = Object.keys(nice_veggie_name);

    div.innerHTML += "<strong>Orte</strong></br></br>";

    // loop through our density intervals and generate a label with a colored square for each interval

    for (var i = 0; i < labels.length; i++) {
      div.innerHTML +=
        '<i style="background:' +
        getColor(labels[i]) +
        '"></i> ' +
        nice_name[labels[i]] +
        " </br> ";
    }

    div.innerHTML += "</br><strong>Vegetation</strong></br></br>";

    for (var i = 0; i < veggieLabels.length; i++) {
      div.innerHTML +=
        '<i style="background:' +
        getVegetationColor(veggieLabels[i]) +
        '"></i> ' +
        nice_veggie_name[veggieLabels[i]] +
        " </br> ";
    }

    return div;
  };

  legend.addTo(map);

  await all_locations();

  async function changeMap({ label, value, map }) {
    if (multiPoint != null && location_isOn) {
      multiPoint.eachLayer(function (layer) {
        if (label == "Alle" || layer.feature.geometry.day == label) {
          map.addLayer(layer);
        } else {
          map.removeLayer(layer);
        }
      });
    }

    if (multiPointVeggie != null && vegetation_isOn) {
      multiPointVeggie.eachLayer(function (layer) {
        if (label == "Alle" || layer.feature.geometry.day == parseInt(label)) {
          map.addLayer(layer);
        } else {
          map.removeLayer(layer);
        }
      });
    }

    if (routes_multiLine != null && route_isOn) {
      routes_multiLine.eachLayer(function (layer) {
        if (label == "Alle" || layer.feature.geometry.name == label) {
          map.addLayer(layer);
        } else {
          map.removeLayer(layer);
        }
      });
    }
    multiPoint.bringToFront();
    multiPointVeggie.bringToFront();
  }

  timelineSlider = L.control
    .timelineSlider({
      timelineItems: ["Alle", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
      changeMap: changeMap,
      labelWidth: "40px",
      position: "bottomleft",
    })
    .addTo(map);

  layer_control = L.control
    .layers(null, {
      Orte: multiPoint,
      Routen: routes_multiLine,
    })
    .addTo(map);
  layer_control.addOverlay(multiPointVeggie, "Vegetation");
  map.on("overlayadd", function (eventLayer) {
    if (eventLayer.name === "Orte") {
      location_isOn = true;
    } else if (eventLayer.name === "Routen") {
      route_isOn = true;
    } else {
      vegetation_isOn = true;
    }
    let label = $($(".range-labels")[0]).children(".active")[0].innerHTML;
    changeMap({ label: label, value: null, map: map });
  });

  map.on("overlayremove", function (eventLayer) {
    if (eventLayer.name === "Orte") {
      location_isOn = false;
    } else if (eventLayer.name === "Routen") {
      route_isOn = false;
    } else {
      vegetation_isOn = false;
    }
  });
}

initMap();
