const DeepSummarizeAnyPage = require('../index');

describe('DeepSummarizeAnyPage Adapter', () => {
  it('summarizes a simple web page (dev backend)', async () => {
    process.env.ECL_BACKEND_PROVIDER = 'UNSIGNED-DEV';
    const result = await DeepSummarizeAnyPage.summarize('https://example.com');
    expect(result).toHaveProperty('summary');
  });

  it('summarizes a web page (prod backend)', async () => {
    process.env.ECL_BACKEND_PROVIDER = 'PROD';
    const result = await DeepSummarizeAnyPage.summarize('https://example.com');
    expect(result).toHaveProperty('summary');
  });
});