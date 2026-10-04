// Only explicitly supported public settings are written into the browser bundle.
export function gameConfig(env = process.env) {
  const rawGems = env.RDFZ_INITIAL_GEMS ?? '3000';
  const rawUnlimited = env.RDFZ_UNLIMITED_GEMS ?? 'false';
  if (!/^\d+$/.test(rawGems) || !Number.isSafeInteger(Number(rawGems))) {
    throw new Error('RDFZ_INITIAL_GEMS must be a non-negative safe integer');
  }
  if (!['true', 'false'].includes(rawUnlimited)) {
    throw new Error('RDFZ_UNLIMITED_GEMS must be true or false');
  }
  return {initialGems:Number(rawGems), unlimitedGems:rawUnlimited === 'true'};
}
