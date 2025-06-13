import { generate } from '../src/api.js';

global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ response: 'test' })
  })
);

test('generate calls backend', async () => {
  const data = await generate('hello', 'basic_gpt');
  expect(fetch).toHaveBeenCalled();
  expect(data.response).toBe('test');
});
