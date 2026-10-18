import { expect, test } from "@playwright/test";

// Point de départ pour le TP : ces tests décrivent le comportement existant.
// Ajoutez les vôtres à partir de vos scénarios d'acceptation.

test("l'API renvoie tous les profils", async ({ request }) => {
  const res = await request.get("/api/cvs");
  expect(res.ok()).toBeTruthy();
  const body = await res.json();
  expect(body.total).toBe(24);
  expect(body.cvs[0]).toMatchObject({ id: "cv-001", prenom: "Léa", nom: "Martin" });
});

test("l'API répond 404 pour un profil inconnu", async ({ request }) => {
  const res = await request.get("/api/cvs/cv-999");
  expect(res.status()).toBe(404);
});

test("la page d'accueil liste tous les profils", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Tous les profils" })).toBeVisible();
  await expect(page.getByTestId("cv-card")).toHaveCount(24);
});

test("une fiche affiche le profil et son CV", async ({ page }) => {
  await page.goto("/");
  await page.getByTestId("cv-card").filter({ hasText: "N'Diaye" }).click();
  await expect(page).toHaveURL(/\/cvs\/cv-010$/);
  await expect(page.getByRole("heading", { name: /Mathis N'Diaye/ })).toBeVisible();
  await expect(page.getByTestId("cv-pdf")).toHaveAttribute("src", "/api/cvs/cv-010/cv");

  const pdf = await page.request.get("/api/cvs/cv-010/cv");
  expect(pdf.headers()["content-type"]).toBe("application/pdf");
});

test("le bouton change de thème et le choix est mémorisé", async ({ page }) => {
  await page.emulateMedia({ colorScheme: "light" });
  await page.goto("/");
  await page.getByTestId("theme-toggle").click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await page.reload();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
});
