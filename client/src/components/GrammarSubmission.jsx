import { useState } from "react";
import { AudioElement } from "./AudioRecorder";
import { ManualGrammarSubmission } from "./ManualGrammarEntry";

export function GrammarSubmission() {
    const [tab, setTab] = useState(0);

    return (
        <div>
            <div>
                <button onClick={() => setTab(0)}>Record Audio</button>
                <button onClick={() => setTab(1)}>Add Entry for Saved Audio</button>
            </div>
            <>
            {tab === 0 && (
                <div>
                    <AudioElement />
                </div>
            )}
            {tab === 1 && (
                <div>
                    <ManualGrammarSubmission />
                </div>
            ) }
            </>
        </div>
        
    )
}