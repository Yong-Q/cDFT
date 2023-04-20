import os
import string

if __name__ == "__main__":
    ngrid = 60  # maxgrid
    dl = 0.5  # grid density
    deltamax = 2.0
    name1=0
    Special_case=0
    epsilongas1 = 36.7
    sigmagas1 = 2.958
    massgas = 2.0158
    bulkdensitygas1 = 0.01
    name2=1
    epsilongas2 = 36.7
    sigmagas2 = 2.958
    bulkdensitygas2 = 0.01
    temperature = 303.0
    Kind_of_gas=2
    kapa = 0.99  # weight for picard iteration for last step
    torr = 5.0
    readvext = 0  # 1 for no calculation external field, 0 for calculation, for each material only need once
    EOS = 1  # 1 for MBWR, 0 for FMSA
    DiffEOS = 1
    cutdft = 12.9  # cutoff in unit Angstrom
    Mass=3.2945 #平均摩尔质量
    Ds_Knudsen=7.598360908038765e-07
    MFV_parameter=1.8786838799311705
    folder_path = './cof/example'  # 文件夹路径

    for file in os.scandir(folder_path):
        # 如果文件是一个普通文件并且具有 ".cif" 扩展名
        if file.is_file() and file.name.endswith('.cif'):
            # 打开文件并进行处理
            with open(file.path, 'r') as pdbfile:
                # pdbfile = open(file_name, 'r')
               # print(file.name)
                aid = -1
                countline = 0
                tot = 180000  # estimate maximum atom numbers in MOF unit cell
                atom_data = [['' for i in range(7)] for j in range(tot)]
                for line in pdbfile:
                    countline = countline + 1
                    if (countline <= 4):
                        continue
                    elif (countline >= 11) and (countline <= 19):
                        continue
                    elif line.split()[0] == 'loop_':
                        break
                    elif line.split()[0] == '_cell_length_a':
                        lxa = float(line.split()[1])
                        continue
                    elif line.split()[0] == '_cell_length_b':
                        lyb = float(line.split()[1])
                        continue
                    elif line.split()[0] == '_cell_length_c':
                        lzc = float(line.split()[1])
                        continue
                    elif line.split()[0] == '_cell_angle_alpha':
                        alpha = float(line.split()[1])
                        continue
                    elif line.split()[0] == '_cell_angle_beta':
                        beta = float(line.split()[1])
                        continue
                    elif line.split()[0] == '_cell_angle_gamma':
                        gamma = float(line.split()[1])
                        continue
                    else:
                        aid = aid + 1
                        atom_data[aid][0] = line.split()[1]  # element type
                        atom_data[aid][1] = line.split()[2]  # x
                        atom_data[aid][2] = line.split()[3]  # y
                        atom_data[aid][3] = line.split()[4]  # z
                        fffile = open('./data_ff_UFF', 'r')
                        for line in fffile:
                            if (line.split()[0] == atom_data[aid][0]):
                                atom_data[aid][4] = line.split()[1]  # sigma (A)
                                atom_data[aid][5] = line.split()[2]  # epsilon (K)
                                atom_data[aid][6] = line.split()[3]  # mass (g/mol)
                                break
                        fffile.close()
                pdbfile.close()
                cutdft = 12.90
                file_ext: tuple
                filename: tuple
                (filename, file_ext) = os.path.splitext(file.name)
                new_file_name = filename + ".dat"
                if os.path.exists('inputcdf'):
                    pass
                # 创建input文件夹
                else:
                    os.makedirs('inputcdf')

                # 将文件写入到input子文件夹中
                inputfile = open(os.path.join('inputcdf', new_file_name), 'w')
                # inputfile = open(./input/new_file_name, 'w')
                inputfile.write('Nmaxx Nmaxy Nmaxz\n')
                inputfile.write('%d   %d   %d\n' % (ngrid, ngrid, ngrid))
                inputfile.write('Lxa Lyb Lzc dL\n')
                inputfile.write('%f   %f   %f   %f\n' % (lxa, lyb, lzc, dl))
                inputfile.write('Alpha Beta Gamma\n')
                inputfile.write('%f   %f   %f\n' % (alpha, beta, gamma))
                inputfile.write('Temperature(K) Kapa Delta_Max Torr\n')
                inputfile.write('%f   %f    %f    %f\n' % (temperature, kapa, deltamax, torr))
                inputfile.write('Kind_of_gas\n')
                inputfile.write('%d\n'%(Kind_of_gas))
                inputfile.write('Name Epsilon(K) Sigma(A) Bulk_Density(molec/A^3)\n')
                inputfile.write(' %d    %f    %f    %f\n' % ( name1,  epsilongas1, sigmagas1, bulkdensitygas1))
                inputfile.write(' %d    %f    %f    %f\n' % ( name2, epsilongas2, sigmagas2, bulkdensitygas2))
                inputfile.write('Special_case\n')
                inputfile.write('%d\n'%(Special_case))
                inputfile.write('Id1 Id2 Epsilon(K) Sigma(A)\n')

                inputfile.write('Read_Vext  EOS    Cutoff Diff_EOS\n')
                inputfile.write('%d    %d     %f   %d\n' % (readvext, EOS, cutdft, DiffEOS))
                inputfile.write('Mass(g/mol) Ds_Knudsen(m^2/s) MFV_parameter\n')
                inputfile.write('%f    %f    %f\n' % (Mass, Ds_Knudsen, MFV_parameter))
                inputfile.write('Kind_of_atoms\n')
                inputfile.write('%d\n' % (aid + 1))
                inputfile.write('ID diameter(A) Epsilon(K)\n')
                massmof = 0.0
                for i in range(0, aid + 1):
                    inputfile.write('%d    %f    %f\n' % ((i + 1), float(atom_data[i][4]), float(atom_data[i][5])))
                    massmof = massmof + float(atom_data[i][6])
                inputfile.write('Number_of_atoms Mass_MOF(g/mol)  Mass_Gas(g/mol)\n')
                inputfile.write('%d   %f   %f\n' % ((aid + 1), massmof, massgas))
                inputfile.write('ID x y z\n')
                for i in range(0, aid + 1):
                    inputfile.write('%d   %f    %f    %f\n' % (
                        (i + 1), float(atom_data[i][1]) * lxa, float(atom_data[i][2]) * lyb,
                        float(atom_data[i][3]) * lzc))
                inputfile.close()
                os.system('./adsorption > runout.dat')
# os.system('cat output.dat')
