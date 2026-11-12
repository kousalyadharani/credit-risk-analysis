#!/usr/bin/env python3
"""Clean numeric credit data and produce deterministic k-means segments."""
import argparse,csv,json,math,random
from pathlib import Path

def clean(rows,features):
 out=[]
 for i,row in enumerate(rows):
  try: vals=[float(row[k]) for k in features]
  except (KeyError,ValueError,TypeError): continue
  if any(not math.isfinite(x) for x in vals):continue
  out.append({"source_row":i+1,"values":vals,"id":row.get("id",str(i+1))})
 return out
def kmeans(points,k=3,seed=7,iterations=100):
 if not points or k<1 or k>len(points):raise ValueError("k must be between 1 and number of rows")
 dims=len(points[0]); means=[sum(p[j] for p in points)/len(points) for j in range(dims)]; scales=[math.sqrt(sum((p[j]-means[j])**2 for p in points)/len(points)) or 1 for j in range(dims)]; z=[[(p[j]-means[j])/scales[j] for j in range(dims)] for p in points]
 rng=random.Random(seed); centers=[z[i][:] for i in rng.sample(range(len(z)),k)]; labels=[0]*len(z)
 for _ in range(iterations):
  new=[min(range(k),key=lambda c:sum((p[j]-centers[c][j])**2 for j in range(dims))) for p in z]
  updated=[]
  for c in range(k):
   members=[z[i] for i,l in enumerate(new) if l==c]
   updated.append([sum(p[j] for p in members)/len(members) if members else z[rng.randrange(len(z))][j] for j in range(dims)])
  if new==labels and updated==centers:break
  labels,centers=new,updated
 return labels
def analyze(rows,features,k=3):
 data=clean(rows,features)
 if not data:raise ValueError("No complete numeric rows")
 labels=kmeans([r["values"] for r in data],min(k,len(data)))
 return [{"id":r["id"],"source_row":r["source_row"],"segment":int(c)} for r,c in zip(data,labels)]
def main():
 p=argparse.ArgumentParser();p.add_argument("input",type=Path);p.add_argument("--features",required=True,help="comma-separated numeric field names");p.add_argument("--clusters",type=int,default=3);p.add_argument("--output",type=Path,default=Path("segments.json"));a=p.parse_args()
 with a.input.open(newline="",encoding="utf-8-sig") as f:rows=list(csv.DictReader(f))
 result=analyze(rows,[x.strip() for x in a.features.split(",")],a.clusters);a.output.write_text(json.dumps(result,indent=2)+"\n");print(f"Segmented {len(result)} complete records")
if __name__=="__main__":main()
