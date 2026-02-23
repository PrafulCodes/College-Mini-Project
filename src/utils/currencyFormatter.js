// Currency formatter utility
export function formatCurrency(amount, currency = "INR") {
  if (typeof amount !== "number") return amount;
  let options = {};
  switch (currency) {
    case "USD":
      options = { style: "currency", currency: "USD", minimumFractionDigits: 2 };
      break;
    case "EUR":
      options = { style: "currency", currency: "EUR", minimumFractionDigits: 2 };
      break;
    case "INR":
    default:
      options = { style: "currency", currency: "INR", minimumFractionDigits: 0, maximumFractionDigits: 0 };
      break;
  }
  return new Intl.NumberFormat(
    currency === "INR" ? "en-IN" : currency === "EUR" ? "en-IE" : "en-US",
    options
  ).format(amount);
}
