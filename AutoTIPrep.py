import os
import warnings
import subprocess
import shutil

def check_environment():
    # 定义要检查的命令
    commands = ['parmed', 'tleap', 'antechamber']
    # 定义要检查的文件
    required_files = ['leap_gas_template.in', 'leap_water_template.in', 'parmed_devdw_template.in',\
                    'group_file_template.group', 'sub_template.sh']

    # 检查每个命令是否存在于环境变量中
    print("Checking environment variables...")
    for command in commands:
        command_path = os.popen(f'which {command}').read().strip()
        if command_path:
            print(f"{command} found at: {command_path}")
        else:
            raise EnvironmentError(f"{command} not found in environment variables")

    # 获取脚本所在的文件夹路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 检查所需文件是否存在于脚本所在的文件夹下
    for file in required_files:
        file_path = os.path.join(script_dir, file)
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"{file} not found in script directory: {script_dir}")
    
    print("\n")

def find_directories():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本的绝对路径
    directories = [os.path.join(script_dir, d) for d in os.listdir(script_dir) if os.path.isdir(os.path.join(script_dir, d)) and not d.startswith('.') and d != 'mdin']
    return directories

def check_files(directory, mol2files, frcmodfiles):
    # 删除所有非.mol2和非.frcmod结尾的文件
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path) and (not (file.endswith('.mol2') or file.endswith('.frcmod')) or file.endswith('_dechg.mol2')):
            os.remove(file_path)

    # 定义所需文件的扩展名及其对应的变量
    required_files = {'.mol2': [], '.frcmod': []}

    # 获取目录下所有文件
    files = os.listdir(directory)

    # 检查每个所需扩展名的文件是否存在
    for extension, file_list in required_files.items():
        # 添加当前扩展名的所有文件到对应列表
        for file in files:
            if file.endswith(extension):
                file_list.append(file)
        
        # 如果对应扩展名的文件列表为空，则发出警告
        if not file_list:
            warnings.warn(f"No file with {extension} extension found in {directory}")

    # 更新外部列表
    mol2files.extend(required_files['.mol2'])

    # 更新frcmodfiles列表，排除solvent.frcmod文件
    frcmodfiles.extend([f for f in required_files['.frcmod'] if f != 'solvent.frcmod'])

def generate_decharge_mol2(directory, mol2name, mol2_dechg_files ,atomnumlist):
    # 定义开始和结束标记
    start_marker = "@<TRIPOS>ATOM"
    end_marker = "@<TRIPOS>BOND"
    
    # 初始化标记
    in_atom_section = False
    
    # 读取原始文件内容
    path = os.path.join(directory, mol2name)
    with open(path, 'r') as file:
        lines = file.readlines()
    
    atomnumlist.append(lines[2].split()[0])
    mol2_dechg_files.append(mol2name.split('.')[0] + '_dechg.mol2')

    # 修改文件内容
    modified_lines = []
    for line in lines:
        if line.strip() == start_marker:
            in_atom_section = True
        elif line.strip() == end_marker:
            in_atom_section = False
        
        if in_atom_section and line.strip() and line.strip() != start_marker:
            parts = line.split()
            parts[-1] = "0.000000"  # 替换最后一列为0.000000
            line = ' '.join(parts) + '\n'
        
        modified_lines.append(line)
    
    # 输出修改后的文件
    output_path = os.path.join(directory, mol2_dechg_files[-1])
    with open(output_path, 'w') as file:
        file.writelines(modified_lines)

def generate_tleap():
    water_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'leap_water_template.in')
    gas_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'leap_gas_template.in')

    for directory, mol2name, frcmodname, mol2_dechg_name in zip(directories, mol2files, frcmodfiles, mol2_dechg_files):
        # 生存tleap输入文件 （Water）
        wat_chg_replacements = {
            '{frcmod_FILE}': f'{frcmodname}',
            '{mol2_FILE}': f'{mol2name}',
            '{prmtop_FILE}': f'{mol2name.split(".")[0]}_wat.prmtop',
            '{inpcrd_FILE}': f'crd_wat.inpcrd',
        }

        gas_chg_replacements = {
            '{frcmod_FILE}': f'{frcmodname}',
            '{mol2_FILE}': f'{mol2name}',
            '{prmtop_FILE}': f'{mol2name.split(".")[0]}_gas.prmtop',
            '{inpcrd_FILE}': f'crd.inpcrd',
        }

        wat_dechg_replacements = {
            '{frcmod_FILE}': f'{frcmodname}',
            '{mol2_FILE}': f'{mol2name}',
            '{prmtop_FILE}': f'{mol2_dechg_name.split(".")[0]}_wat.prmtop',
            '{inpcrd_FILE}': f'crd.inpcrd',
        }

        gas_dechg_replacements = {
            '{frcmod_FILE}': f'{frcmodname}',
            '{mol2_FILE}': f'{mol2name}',
            '{prmtop_FILE}': f'{mol2_dechg_name.split(".")[0]}_gas.prmtop',
            '{inpcrd_FILE}': f'crd_gas.inpcrd',
        }

        prm_wat.append(f'{mol2name.split(".")[0]}_wat.prmtop')
        prm_gas.append(f'{mol2name.split(".")[0]}_gas.prmtop')
        prm_dechg_wat.append(f'{mol2_dechg_name.split(".")[0]}_wat.prmtop')
        prm_dechg_gas.append(f'{mol2_dechg_name.split(".")[0]}_gas.prmtop')

        wat_output_path = os.path.join(directory, 'leap_water.in')
        gas_output_path = os.path.join(directory, 'leap_gas.in')
        wat_dechg_output_path = os.path.join(directory, 'leap_water_dechg.in')
        gas_dechg_output_path = os.path.join(directory, 'leap_gas_dechg.in')

        # 生成水模拟的tleap输入文件
        with open(water_template, 'r') as file:
            template = file.read()

        for placeholder, value in wat_chg_replacements.items():
            template = template.replace(placeholder, value)
        
        with open(wat_output_path, 'w') as file:
            file.write(template)

        # 生成气相模拟的tleap输入文件
        with open(gas_template, 'r') as file:
            template = file.read()
        
        for placeholder, value in gas_chg_replacements.items():
            template = template.replace(placeholder, value)

        with open(gas_output_path, 'w') as file:
            file.write(template)

        # 生成去电荷水模拟的tleap输入文件
        with open(water_template, 'r') as file:
            template = file.read()
        
        for placeholder, value in wat_dechg_replacements.items():
            template = template.replace(placeholder, value)

        with open(wat_dechg_output_path, 'w') as file:
            file.write(template)

        # 生成去电荷气相模拟的tleap输入文件
        with open(gas_template, 'r') as file:
            template = file.read()

        for placeholder, value in gas_dechg_replacements.items():
            template = template.replace(placeholder, value)
        
        with open(gas_dechg_output_path, 'w') as file:
            file.write(template)
        
def tleap_build():
    for directory in directories:
        parent_directory = os.path.dirname(directory)  # Find the parent directory
        # List all files in the parent directory
        files_in_parent = [f for f in os.listdir(parent_directory) if os.path.isfile(os.path.join(parent_directory, f))]
        # Filter and copy .frcmod, .prepi, .pdb files to the target directory
        for file in files_in_parent:
            if file.endswith(('.frcmod', '.prepi', '.pdb')):
                shutil.copy(os.path.join(parent_directory, file), directory)
        # Change to the target directory and run the commands
        os.chdir(directory)
        print(f"Building system in {directory}...")
        subprocess.run(['tleap', '-f', 'leap_water.in'], check=True, capture_output=True, text=True)
        subprocess.run(['tleap', '-f', 'leap_gas.in'], check=True, capture_output=True, text=True)
        subprocess.run(['tleap', '-f', 'leap_water_dechg.in'], check=True, capture_output=True, text=True)
        subprocess.run(['tleap', '-f', 'leap_gas_dechg.in'], check=True, capture_output=True, text=True)

def generate_parmed():
    parmed_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parmed_devdw_template.in')
    prm_devdw = []

    for directory, mol2name, atomnums in zip(directories, mol2files, atomnumlist):
        devdw_wat_output_path = os.path.join(directory, 'parmed_devdw_wat.in')
        devdw_gas_output_path = os.path.join(directory, 'parmed_devdw_gas.in')
        
        # 生成水模拟的parmed输入文件
        with open(parmed_template, 'r') as file:
            template = file.read()

        prm_wat_devdw.append(mol2name.split('.')[0] + '_wat_devdw.prmtop')
        template = template.replace('{devdw_FILE}', mol2name.split('.')[0] + '_wat_devdw.prmtop')

        # 数目要和solvent的原子数目一致
        solvent_atom = 27 # octanol
        parmed_command = []
        for i in range(1, int(atomnums) + 1):
            for j in range(1, int(solvent_atom) + 1):
                parmed_command.append(f'changeLJPair @{i} @{int(atomnums)+j} 0.0 0.0')
  


        complete_command = '\n'.join(parmed_command) + '\n' + template

        with open(devdw_wat_output_path, 'w') as file:
            file.write(complete_command)

        # 生成气相模拟的parmed输入文件
        with open(parmed_template, 'r') as file:
            template = file.read()

        prm_gas_devdw.append(mol2name.split('.')[0] + '_gas_devdw.prmtop')
        template = template.replace('{devdw_FILE}', mol2name.split('.')[0] + '_gas_devdw.prmtop')

        parmed_command = []

        complete_command = '\n'.join(parmed_command) + '\n' + template

        with open(devdw_gas_output_path, 'w') as file:
            file.write(complete_command)
        
def parmed_run():
    for directory, dechg_wat, dechg_gas in zip(directories, prm_dechg_wat, prm_dechg_gas):
        os.chdir(directory)
        subprocess.run(['parmed', f'{dechg_wat}', 'parmed_devdw_wat.in'], check=True, capture_output=True, text=True)
        subprocess.run(['parmed', f'{dechg_gas}', 'parmed_devdw_gas.in'], check=True, capture_output=True, text=True)

def generate_group_file():
    for directory, wat_prm, wat_de_prm, gas_prm, gas_de_prm in zip(directories, prm_wat, prm_wat_devdw, prm_gas, prm_gas_devdw):
        os.chdir(directory)
        if not os.path.exists('group'):
            os.mkdir('group')
        else:
            os.chdir('group')
            for file in os.listdir('.'):
                os.remove(file)
            os.chdir('..')
    
        for i in range(1, 10):
            wat_de_replacements = {
                '{mdin_FILE}': f'wat_md{i}_k6.in',
                '{prm_FILE1}': f'{wat_prm}',
                '{prm_FILE2}': f'{wat_de_prm}',
                '{CRD_FILE}': f'md_final_wat.rst' if i == 1 else f'rst_wat{i-1}.rst',
                '{out_FILE1}': f'output_wat{i}.out',
                '{out_FILE2}': f'output_de_wat{i}.out',
                '{info_FILE1}': f'info_wat{i}.out',
                '{info_FILE2}': f'info_de_wat{i}.out',
                '{trj_FILE1}': f'trj_wat{i}.nc',
                '{trj_FILE2}': f'trj_de_wat{i}.nc',
                '{rst_FILE1}': f'rst_wat{i}.rst',
                '{rst_FILE2}': f'rst_de_wat{i}.rst',
            }

            gas_de_replacements = {
                '{mdin_FILE}': f'gas_md{i}_k6.in',
                '{prm_FILE1}': f'{gas_prm}',
                '{prm_FILE2}': f'{gas_de_prm}',
                '{CRD_FILE}': f'gas_min1.rst' if i == 1 else f'rst_gas{i-1}.rst',
                '{out_FILE1}': f'output_gas{i}.out',
                '{out_FILE2}': f'output_de_gas{i}.out',
                '{info_FILE1}': f'info_gas{i}.out',
                '{info_FILE2}': f'info_de_gas{i}.out',
                '{trj_FILE1}': f'trj_gas{i}.nc',
                '{trj_FILE2}': f'trj_de_gas{i}.nc',
                '{rst_FILE1}': f'rst_gas{i}.rst',
                '{rst_FILE2}': f'rst_de_gas{i}.rst',
            }
            
            grp_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'group_file_template.group')
            with open(grp_template, 'r') as file:
                template = file.read()
            
            dechg = template
            for placeholder, value in wat_de_replacements.items():
                dechg = dechg.replace(placeholder, value)
            
            devdw = template
            for placeholder, value in gas_de_replacements.items():
                devdw = devdw.replace(placeholder, value)
            
            wat_path = os.path.join(directory, 'group', f'wat_s{i}.group')
            gas_path = os.path.join(directory, 'group', f'gas_s{i}.group')
        
            with open(wat_path, 'w') as file:
                file.write(dechg)
            
            with open(gas_path, 'w') as file:
                file.write(devdw)

def find_and_sort_in_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本的绝对路径
    mdin_dir = os.path.join(script_dir, 'mdin')  # 构建mdin文件夹的路径

    k6_in_files = []  # 存储以_k6.in结尾的文件名
    other_in_files = []  # 存储其他以.in结尾的文件名

    # 遍历mdin文件夹下的所有文件
    for file in os.listdir(mdin_dir):
        if file.endswith('_k6.in'):
            k6_in_files.append(file)
        elif file.endswith('.in') and not file.endswith('_k6.in'):  # 排除以_k6.in结尾的文件
            other_in_files.append(file)

    # 对两个列表进行排序
    k6_in_files.sort()
    other_in_files.sort()

    return k6_in_files, other_in_files

def generate_slurm_script(template_path, directory, wat_top, gas_top):
    # 读取模板文件内容
    with open(template_path, 'r') as file:
        template = file.read()

    wat_template = template.replace('--job-name=xujian', f'--job-name=wat_{wat_top.split("_")[0]}')
    gas_template = template.replace('--job-name=xujian', f'--job-name=gas_{gas_top.split("_")[0]}')

    ANI_enegies = '/ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI'
    cMD_enegies = '/ix1/jwang/tan77/xujian/software/amber22_ori/amber22/bin/sander.MPI'
    # 示例命令列表
    commands_wat = [
        "echo \"Water Minimization 1\"",
        f"mpirun -np 16 {cMD_enegies} -O -i ../mdin/general/wat_min1.in -p {wat_top} -c crd_wat.inpcrd   -o output_wat_min1.out -r wat_min1.rst",
        "sleep 2",
        "echo \"Water Minimization 2\"",
        f"mpirun -np 16 {cMD_enegies} -O -i ../mdin/general/wat_min2.in -p {wat_top} -c wat_min1.rst -o output_wat_min2.out -r wat_min2.rst",
        "sleep 2",
        "echo \"Water cMD Simulation 1\"",
        f"mpirun -np 16 {cMD_enegies} -O -i ../mdin/general/wat_md_1.in -p {wat_top} -c wat_min2.rst -o output_wat_md1.out  -r wat_md1.rst",
        "sleep 2",
        "echo \"Water ANI-MD Simulation\"",
        f"mpirun -np 16 {ANI_enegies} -O -i ../mdin/general/wat_md_2.in -p {wat_top} -c wat_md1.rst  -o output_wat_md2.out  -r md_final_wat.rst",
        "sleep 2",
        "echo \"Water Simulation 1\"",
        f"mpirun -np 16 {ANI_enegies}  -ng 16 -groupfile ./group/wat_s1.group",
        "sleep 2",
        "echo \"Water Simulation 2\"",
        f"mpirun -np 16 {ANI_enegies}  -ng 16 -groupfile ./group/wat_s2.group",
        "sleep 2",
        "echo \"Water Simulation 3\"",
        f"mpirun -np 16 {ANI_enegies}  -ng 16 -groupfile ./group/wat_s3.group",
        "sleep 2",
        "echo \"Water Simulation 4\"",
        f"mpirun -np 16 {ANI_enegies}  -ng 16 -groupfile ./group/wat_s4.group",
        "sleep 2",
        "echo \"Water Simulation 5\"",
        f"mpirun -np 16 {ANI_enegies}  -ng 16 -groupfile ./group/wat_s5.group",
        "sleep 2",
        "echo \"Water Simulation 6\"",
        f"mpirun -np 16 {ANI_enegies}  -ng 16 -groupfile ./group/wat_s6.group",
        "sleep 2",
        "echo \"Water Simulation 7\"",
        f"mpirun -np 16 {ANI_enegies}  -ng 16 -groupfile ./group/wat_s7.group",
        "sleep 2",
        "echo \"Water Simulation 8\"",
        f"mpirun -np 16 {ANI_enegies}  -ng 16 -groupfile ./group/wat_s8.group",
        "sleep 2",
        "echo \"Water Simulation 9\"",
        f"mpirun -np 16 {ANI_enegies}  -ng 16 -groupfile ./group/wat_s9.group",
        "sleep 2",
    ]

    commands_gas = [
        "echo \"Gas Minimization 1\"",
        f"mpirun -np 1 {cMD_enegies} -O -i ../mdin/general/gas_min.in -p {gas_top} -c crd_gas.inpcrd   -o output_gas_min1.out -r gas_min1.rst",
        "sleep 2",
        "echo \"Gas Simulation 1\"",
        f"mpirun -np 2 {ANI_enegies} -ng 2 -groupfile ./group/gas_s1.group",
        "sleep 2",
        "echo \"Gas Simulation 2\"",
        f"mpirun -np 2 {ANI_enegies}  -ng 2 -groupfile ./group/gas_s2.group",
        "sleep 2",
        "echo \"Gas Simulation 3\"",
        f"mpirun -np 2 {ANI_enegies}  -ng 2 -groupfile ./group/gas_s3.group",
        "sleep 2",
        "echo \"Gas Simulation 4\"",
        f"mpirun -np 2 {ANI_enegies}  -ng 2 -groupfile ./group/gas_s4.group",
        "sleep 2",
        "echo \"Gas Simulation 5\"",
        f"mpirun -np 2 {ANI_enegies}  -ng 2 -groupfile ./group/gas_s5.group",
        "sleep 2",
        "echo \"Gas Simulation 6\"",
        f"mpirun -np 2 {ANI_enegies}  -ng 2 -groupfile ./group/gas_s6.group",
        "sleep 2",
        "echo \"Gas Simulation 7\"",
        f"mpirun -np 2 {ANI_enegies}  -ng 2 -groupfile ./group/gas_s7.group",
        "sleep 2",
        "echo \"Gas Simulation 8\"",
        f"mpirun -np 2 {ANI_enegies}  -ng 2 -groupfile ./group/gas_s8.group",
        "sleep 2",
        "echo \"Gas Simulation 9\"",
        f"mpirun -np 2 {ANI_enegies}  -ng 2 -groupfile ./group/gas_s9.group",
        "sleep 2",
        "gzip *.trj",
        "sleep 10"
    ]

    # 将新内容附加到模板文件的末尾
    script_content_wat = wat_template + '\n' + '\n'.join(commands_wat)
    script_content_gas = gas_template + '\n' + '\n'.join(commands_gas)


    # 将结果写入新的sub.sh文件
    wat_output_path = os.path.join(directory, 'sub_wat.sh')
    gas_output_path = os.path.join(directory, 'sub_gas.sh')

    with open(wat_output_path, 'w') as file:
        file.write(script_content_wat)

    with open(gas_output_path, 'w') as file:
        file.write(script_content_gas)


if __name__ == '__main__':

    print("AutoTIPrep.py is running as a script")
    print("\n")

    # Step 1: Check the environment
    check_environment()

    # Step 2: Find all directories in the current directory
    print("Finding directories...")
    directories = find_directories()
    print("Totaly found directories: ", len(directories))
    print("\n") 

    # Step 3: Check the files in each directory
    # Initialize lists to store mol2 and frcmod files
    print("Checking files in each directory...")
    print("\n")
    mol2files = []
    frcmodfiles = []
    for directory in directories:
        check_files(directory, mol2files, frcmodfiles)
    print(frcmodfiles)

    # Step 4: Generate decharged mol2 files
    print("Generating decharged mol2 files...")
    print("\n")
    atomnumlist = []
    mol2_dechg_files = []
    for directory, mol2name in zip(directories, mol2files):
        generate_decharge_mol2(directory, mol2name, mol2_dechg_files, atomnumlist)

    # Step 5: Generate tleap input files
    print("Generating tleap input files...")
    print("\n")
    prm_wat = []
    prm_gas = []
    prm_dechg_wat = []
    prm_dechg_gas = []
    generate_tleap()

    # Step 6: Build the system through tleap
    print("Building the system through tleap...")
    print("\n")
    tleap_build()

    # Step 7: Build de van der Waals prmtop files
    print("Generating de van der Waals prmtop files...")
    print("\n")
    prm_wat_devdw = []
    prm_gas_devdw = []
    generate_parmed()

    # Step 8: Generate de van der Waals prmtop files
    print("Running parmed to generate de van der Waals prmtop files...")
    print("\n")
    parmed_run()

    # Step 9: Generate the group fils
    print("Generating the group files...")
    print("\n")
    generate_group_file()

    # Step 10: Slurm script
    print("Generating slurm scripts...")
    print("\n")
    for directory, wat_top, gas_top in zip(directories, prm_wat, prm_gas):
        os.chdir(directory)
        slurm_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sub_template.sh')
        slurm_output = os.path.join(directory, 'sub.sh')
        generate_slurm_script(slurm_template, directory, wat_top, gas_top)

    # Step 11: Finish
    print("AutoTIPrep.py has finished running")

