const euros = new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR", maximumFractionDigits: 0 });

/** 48000 → « 48 000 € » */
export function formatRemuneration(value: number): string {
  return euros.format(value);
}

/** « Anne-Sophie », « Le Gall » → « AL » */
export function initials(prenom: string, nom: string): string {
  return (prenom.charAt(0) + nom.charAt(0)).toUpperCase();
}
