const NotionToRFC = require('../index');

describe('NotionToRFC Adapter', () => {
  it('converts Notion document to RFC (dev backend)', async () => {
    process.env.ECL_BACKEND_PROVIDER = 'UNSIGNED-DEV';
    const result = await NotionToRFC.convert('notion-doc-id');
    expect(result).toHaveProperty('rfc');
  });

  it('converts Notion document to RFC (prod backend)', async () => {
    process.env.ECL_BACKEND_PROVIDER = 'PROD';
    const result = await NotionToRFC.convert('notion-doc-id');
    expect(result).toHaveProperty('rfc');
  });
});