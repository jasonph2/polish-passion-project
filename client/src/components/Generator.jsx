import { generatePhrase } from '../api';
export function Generator() {
    const generate = () => {
        const fetching = async () => {
          const data = await generatePhrase();
          console.log(data);
        }
        fetching();
    }
    return (
        <div>
            <button onClick={generate}>Generate</button>
        </div>
    )
}