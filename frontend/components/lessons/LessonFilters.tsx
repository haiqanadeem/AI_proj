import { useState } from "react";

export function LessonFilters({ onFilter }: { onFilter: (diff: string, topic: string) => void }) {
  const [diff, setDiff] = useState("");
  const [topic, setTopic] = useState("");

  const handleApply = () => {
    onFilter(diff, topic);
  };

  return (
    <div className="flex flex-col md:flex-row gap-4 mb-6">
      <div className="flex flex-col">
        <label htmlFor="difficulty" className="text-sm font-medium mb-1">Difficulty</label>
        <select id="difficulty" value={diff} onChange={e => setDiff(e.target.value)} className="p-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary bg-background text-foreground">
          <option value="">All Difficulties</option>
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
      </div>
      <div className="flex flex-col">
        <label htmlFor="topic" className="text-sm font-medium mb-1">Topic</label>
        <select id="topic" value={topic} onChange={e => setTopic(e.target.value)} className="p-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary bg-background text-foreground">
          <option value="">All Topics</option>
          <option value="Python Basics">Python Basics</option>
          <option value="Variables">Variables</option>
          <option value="Control Flow">Control Flow</option>
          <option value="Functions">Functions</option>
          <option value="Data Structures">Data Structures</option>
          <option value="Object-Oriented Programming">Object-Oriented Programming</option>
        </select>
      </div>
      <div className="flex items-end">
        <button onClick={handleApply} className="p-2 bg-primary text-primary-foreground rounded focus:outline-none focus:ring-2 focus:ring-accent font-medium">Apply Filters</button>
      </div>
    </div>
  );
}
