// Given a response, return the JSON data contained in it or throw
// an appropriate error
export async function parseJson(resp) {
  return resp.then(async (resp) => {
    if (!resp.ok) {
      throw new Error(
        await resp
          .json()
          .then((data) => {
            return data.message;
          })
          .catch((_) => {
            return `${resp.status}: ${resp.statusText}`;
          })
      );
    }
    return resp.json();
  });
}
