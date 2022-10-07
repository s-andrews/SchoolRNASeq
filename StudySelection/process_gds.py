# This script takes in an exported GEO search result and reformats it 
# in a way which makes it suitable for inclusion into a spreadsheet to
# allow for triaging and selection of studies.

# The search used for the initial selection was:
# (mus musculus[Organism]) AND "expression profiling by high throughput sequencing"[DataSet Type] AND "knockout"[Title] From 2019/01/01 to 2022/12/31


def main():
    input_file = "gds_result.txt"
    output_file= "gds_spreadsheet.tsv"

    with open(output_file,"wt", encoding="utf8") as out:

        headers = ["Accession","Samples","Title","Description"]
        print("\t".join(headers), file=out)

        with open(input_file,"rt",encoding="utf8") as infh:

            while True:
                title = infh.readline()
                if not title:
                    break

                title = title.strip().split(" ", maxsplit=1)[1]

                description = ""
                organism = ""
                while True:
                    line = infh.readline().strip()
                    if line.startswith("Organism:"):
                        organism = line.split("\t")[1]
                        break

                    description += " "
                    description += line
                
                description = description.replace(" more...","")
                description = description.replace("(Submitter supplied) ","")
                description = description.strip()
                print(organism)
                
                type = infh.readline().split("\t")[1].strip()

                samples = ""

                line = infh.readline()
                if line.startswith("Platform:"):
                    samples = line.strip().split(" ")[2]

                ftp = infh.readline()

                line = infh.readline()

                if line.startswith("SRA Run Selector"):
                    line = infh.readline()

                accession = line.strip().split("\t")[2].split(" ")[1]
                print(accession)

                blank = infh.readline()

                # Filter out stuff we don't want
                if not samples:
                    continue

                if "SuperSeries" in description:
                    continue

                if ";" in type:
                    continue

                if "scRNA" in title or "scRNA" in description:
                    continue

                line = [accession,samples,title,description]

                print("\t".join(line), file=out)



if __name__ == "__main__":
    main()

