import { ProgressResponse } from "@/types/api";

export function KnowledgeTable({ progress }: { progress: ProgressResponse }) {
  return (
    <div className="overflow-x-auto rounded-lg border border-border mt-6 shadow-sm">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="bg-muted text-foreground border-b border-border">
            <th className="p-4 font-bold">Topic</th>
            <th className="p-4 font-bold">Mastery Level</th>
            <th className="p-4 font-bold">Status</th>
          </tr>
        </thead>
        <tbody>
          {progress.knowledge_profile.map((item, idx) => (
            <tr key={idx} className="border-b border-border bg-card hover:bg-muted/50 transition-colors">
              <td className="p-4 font-medium">{item.topic}</td>
              <td className="p-4">
                <div className="flex items-center gap-2">
                  <div className="w-full bg-secondary h-2 rounded-full overflow-hidden">
                    <div className="bg-primary h-full" style={{ width: `${item.mastery_percentage}%` }}></div>
                  </div>
                  <span className="text-sm font-medium">{item.mastery_percentage}%</span>
                </div>
              </td>
              <td className="p-4">
                <span className={`px-2 py-1 rounded text-sm font-medium ${item.status === 'Needs Review' ? 'bg-destructive/20 text-destructive' : 'bg-primary/20 text-primary'}`}>
                  {item.status}
                </span>
              </td>
            </tr>
          ))}
          {progress.knowledge_profile.length === 0 && (
            <tr>
              <td colSpan={3} className="p-4 text-center text-muted-foreground bg-card">No progress data available yet. Complete some lessons!</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
