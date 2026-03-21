const PRSummaryV2 = require('../index');

describe('PRSummaryV2 Adapter', () => {
  it('summarizes a PR using mock API (dev backend)', async () => {
    process.env.ECL_BACKEND_PROVIDER = 'UNSIGNED-DEV';
    const result = await PRSummaryV2.summarize(123);
    expect(result).toHaveProperty('summary');
  });

  it('summarizes a PR using real API (prod backend)', async () => {
    process.env.ECL_BACKEND_PROVIDER = 'PROD';
    const result = await PRSummaryV2.summarize(123);
    expect(result).toHaveProperty('summary');
  });
});