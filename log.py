def read_last_lines(file_name, num_lines=10):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            # Haal de laatste 'num_lines' lijnen op
            last_lines = lines[-num_lines:] if len(lines) >= num_lines else lines
            return last_lines
    except FileNotFoundError:
        print(f"⚠️ Het bestand '{file_name}' bestaat niet.")
        return []
    except Exception as e:
        print(f"⚠️ Fout bij lezen van bestand: {e}")
        return []

if __name__ == "__main__":
    file_name = "test_log.txt"
    last_lines = read_last_lines(file_name)
    
    if last_lines:
        print("\nLaatste 10 lijnen van het logbestand:")
        for line in last_lines:
            print(line.strip())