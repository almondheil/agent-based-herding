def save_output_graph(fname):
    output_x = []
    output_y = []
   
    with open(fname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for line in csv_reader:
            # print(line)
            if "#" in line[0]:
                continue
            if line_count == 0:
                column_names = line # if it's the first line, it holds the titles. IDK what to do with them yet
                pass 
            else:
                output_x.append(float(line[0])) # append the x and y values otherwise
                output_y.append(float(line[1]))
                line_count += 1
                
    plt.scatter(output_x, output_y, s=3)
    plt.title('Prey herds as seen from above')
    plt.xticks([])
    plt.yticks([])
    plt.savefig('%s.png' % fname.split(".")[0]) # save as fname.png, not fname.csv.png
    # if verbose: plt.show()
    plt.show()
