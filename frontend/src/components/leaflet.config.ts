import L from "leaflet";

// Fix the missing marker icon issue in dev environments
delete (L.Icon.Default.prototype as any)._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: "/assets/marker-icon-2x.png",
  iconUrl: "/assets/marker-icon.png",
  shadowUrl: "/assets/marker-shadow.png",
});

// <a href="https://www.flaticon.com/free-icons/red-flag" title="red flag icons">Red flag icons created by Manuel Viveros - Flaticon</a>
// <a href="https://www.flaticon.com/free-icons/flag" title="flag icons">Flag icons created by Pixel perfect - Flaticon</a>