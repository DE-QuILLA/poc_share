# The masterfilelist.txt is not comprehensive (originally over 100mb. i had to cut it)
# import re
import requests
import zipfile
import os
# import pandas as pd

if __name__ == "__main__":

    ## These can be done with a bash script.
    ## But for demonstration purposes... 🥴
    with open('masterfilelist.txt', 'r') as f:
        
        total_size = 0
        total_count = 0

        # every 15 min, the files are uploaded in events-mentions-gkg order
        for line_number, line in enumerate(f, start=1):
            
            clean = line.strip()

            # Get the link string
            # match = re.search(r'(http[s]?://\S+)', clean)
            # if not match:
            #     raise ValueError("NO URL FOUND 👹")
            # url = match.group(1)
            size, checksum, url = clean.split()
            url_1st_part, url_2nd_part, url_3rd_part, dataset, content_type, compression = url.split(".")
            tld, gdelt_ver, dt = url_3rd_part.split("/")


            # We don't need the mentions dataset
            if dataset == "mentions":
                continue

            print(f"URL found: {url}")

            # Download zip
            zip_path = f"{dataset}_{dt}_{line_number}.zip"
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(zip_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            print(f"That'll be {size} dollars (bytes)")

            # Unzip
            extracted_dir = 'raw_csv'
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extracted_dir)
            # Cleanup
            if os.path.exists(zip_path):
                os.remove(zip_path)
            print("Unzip complete")
            print("#---#---#---#---#---#---#---#---#---#")

            total_size += eval(size)
            total_count += 1

            if line_number == 3:
                break

        print(f"Total size: {total_size/1024/1024/1024:.2f} GB")
        print(f"Total count: {total_count} files")
        print("#---#---#---#---#---#---#---#---#---#")

    # CSV inspection
    # csv_files = [f for f in os.listdir(extracted_dir) if f.endswith('.CSV') or f.endswith('.csv')]
    # if not csv_files:
    #     raise FileNotFoundError("NO CSV IN THERE 😇")
            
    # Inspect the first file for col names
    # csv_path = os.path.join('raw_csv', csv_files[0])
    # df = pd.read_csv(csv_path, nrows=5, delimiter='\t', engine='python', header=None)
    # print(df)
    # It doesn't seem to contain col names. 
    # For the data spec, see the notion page https://www.notion.so/1eb90ab6365f807c98b5c96942976b5b